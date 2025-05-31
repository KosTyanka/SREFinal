#!/usr/bin/env python3

import yaml
import docker
import time
import requests
import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from typing import Dict, List, Optional
import subprocess
import signal
import threading
from jinja2 import Template
import msvcrt  # For Windows keyboard input

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChaosCompose:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.docker_client = docker.from_env()
        self.registry = CollectorRegistry()
        self.metrics = self._setup_metrics()
        self.recovery_times: List[float] = []
        self.events: List[Dict] = []
        self.last_known_response = None
        self.skip_wait = False  # Flag to skip waiting period
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def _setup_metrics(self) -> Dict:
        """Initialize Prometheus metrics."""
        return {
            'recovery_time': Gauge(
                f"{self.config['prometheus']['metric_prefix']}_recovery_time_seconds",
                'Time taken for service to recover after chaos injection',
                ['service', 'failure_type'],
                registry=self.registry
            ),
            'failure_count': Gauge(
                f"{self.config['prometheus']['metric_prefix']}_failure_count",
                'Number of chaos events injected',
                ['service', 'failure_type'],
                registry=self.registry
            )
        }

    def _get_container(self, service_name: str) -> Optional[docker.models.containers.Container]:
        """Get container by service name."""
        containers = self.docker_client.containers.list(
            filters={'label': f'com.docker.compose.service={service_name}'}
        )
        return containers[0] if containers else None

    def _check_health(self) -> bool:
        """Check if the service is healthy by making multiple requests."""
        try:
            # Make multiple requests to ensure stability
            for _ in range(3):
                response = requests.get(
                    self.config['health_check']['endpoint'],
                    timeout=self.config['health_check']['timeout_seconds']
                )
                
                if response.status_code != 200:
                    logger.info(f"Health check failed with status code: {response.status_code}")
                    return False

                # Try to parse response as JSON
                try:
                    current_data = response.json()
                    
                    # If this is our first check, store the response
                    if self.last_known_response is None:
                        self.last_known_response = current_data
                        
                    # Compare with last known good response if we have one
                    elif current_data != self.last_known_response:
                        logger.info("Health check response data changed unexpectedly")
                        return False
                        
                except json.JSONDecodeError:
                    logger.info("Health check response is not valid JSON")
                    return False
                
                # Add a small delay between checks
                time.sleep(1)
            
            return True
            
        except requests.RequestException as e:
            logger.info(f"Health check request failed: {str(e)}")
            return False

    def _wait_for_recovery(self, start_time: float) -> float:
        """Wait for service to recover and return recovery time."""
        retries = 0
        while retries < self.config['health_check']['max_retries']:
            if self._check_health():
                recovery_time = time.time() - start_time
                logger.info(f"Service recovered after {recovery_time:.2f} seconds")
                return recovery_time
            
            time.sleep(self.config['health_check']['interval_seconds'])
            retries += 1
            logger.info(f"Health check attempt {retries}/{self.config['health_check']['max_retries']}")
        
        logger.error("Service failed to recover within timeout period")
        return -1

    def inject_chaos(self, scenario: Dict) -> None:
        """Inject chaos according to scenario configuration."""
        service_name = scenario['target_service']
        container = self._get_container(service_name)
        
        if not container:
            logger.error(f"Container for service {service_name} not found")
            return

        for action in scenario['actions']:
            action_type = action['type']
            logger.info(f"Injecting chaos: {action_type} into {service_name}")
            
            start_time = time.time()
            event = {
                'timestamp': datetime.now().isoformat(),
                'service': service_name,
                'action': action_type,
                'start_time': start_time
            }

            try:
                # Store the last known good response before chaos
                try:
                    response = requests.get(
                        self.config['health_check']['endpoint'],
                        timeout=self.config['health_check']['timeout_seconds']
                    )
                    if response.status_code == 200:
                        self.last_known_response = response.json()
                except:
                    pass

                if action_type == 'kill':
                    container.kill(signal=action['signal'])
                    # Wait a bit for the container to fully stop
                    time.sleep(2)
                    # Force restart the container
                    try:
                        container.start()
                        logger.info("Container restarted manually")
                    except Exception as e:
                        logger.error(f"Failed to restart container: {e}")
                        # Try to get a fresh container reference and restart
                        container = self._get_container(service_name)
                        if container:
                            container.start()
                            logger.info("Container restarted with fresh reference")
                elif action_type == 'pause':
                    container.pause()
                    time.sleep(action['duration_seconds'])
                    container.unpause()
                elif action_type == 'network_delay':
                    # Add network delay using tc
                    cmd = f"docker exec {container.id} tc qdisc add dev eth0 root netem delay {action['latency_ms']}ms"
                    subprocess.run(cmd, shell=True, check=True)
                    time.sleep(action['duration_seconds'])
                    cmd = f"docker exec {container.id} tc qdisc del dev eth0 root"
                    subprocess.run(cmd, shell=True, check=True)

                recovery_time = self._wait_for_recovery(start_time)
                event['recovery_time'] = recovery_time
                self.events.append(event)

                # Push metrics to Prometheus
                self.metrics['recovery_time'].labels(
                    service=service_name,
                    failure_type=action_type
                ).set(recovery_time)
                
                self.metrics['failure_count'].labels(
                    service=service_name,
                    failure_type=action_type
                ).inc()

                # Push to Prometheus Pushgateway
                push_to_gateway(
                    self.config['prometheus']['pushgateway_url'],
                    job='chaos_compose',
                    registry=self.registry
                )

            except Exception as e:
                logger.error(f"Error during chaos injection: {e}")
                event['error'] = str(e)
                self.events.append(event)

    def generate_report(self) -> None:
        """Generate test report in specified formats."""
        report_data = {
            'total_events': len(self.events),
            'events': self.events,
            'summary': {
                'total_successful_recoveries': len([e for e in self.events if e.get('recovery_time', -1) > 0]),
                'average_recovery_time': sum([e.get('recovery_time', 0) for e in self.events if e.get('recovery_time', -1) > 0]) / len(self.events) if self.events else 0,
                'max_recovery_time': max([e.get('recovery_time', 0) for e in self.events if e.get('recovery_time', -1) > 0], default=0)
            }
        }

        # Text report
        if 'text' in self.config['test_settings']['report_format']:
            self._generate_text_report(report_data)

        # HTML report
        if 'html' in self.config['test_settings']['report_format']:
            self._generate_html_report(report_data)

    def _generate_text_report(self, data: Dict) -> None:
        """Generate text report."""
        report = f"""
ChaosCompose Test Report
========================
Total Events: {data['total_events']}
Successful Recoveries: {data['summary']['total_successful_recoveries']}
Average Recovery Time: {data['summary']['average_recovery_time']:.2f}s
Maximum Recovery Time: {data['summary']['max_recovery_time']:.2f}s

Detailed Events:
---------------
"""
        for event in data['events']:
            report += f"""
Timestamp: {event['timestamp']}
Service: {event['service']}
Action: {event['action']}
Recovery Time: {event.get('recovery_time', 'N/A')}s
"""
            if 'error' in event:
                report += f"Error: {event['error']}\n"

        with open('chaos_report.txt', 'w') as f:
            f.write(report)
        logger.info("Text report generated: chaos_report.txt")

    def _generate_html_report(self, data: Dict) -> None:
        """Generate HTML report."""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ChaosCompose Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        .event { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>ChaosCompose Test Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Events: {{ data.total_events }}</p>
        <p>Successful Recoveries: {{ data.summary.total_successful_recoveries }}</p>
        <p>Average Recovery Time: {{ "%.2f"|format(data.summary.average_recovery_time) }}s</p>
        <p>Maximum Recovery Time: {{ "%.2f"|format(data.summary.max_recovery_time) }}s</p>
    </div>
    <h2>Detailed Events</h2>
    {% for event in data.events %}
    <div class="event">
        <p><strong>Timestamp:</strong> {{ event.timestamp }}</p>
        <p><strong>Service:</strong> {{ event.service }}</p>
        <p><strong>Action:</strong> {{ event.action }}</p>
        <p><strong>Recovery Time:</strong> {{ "%.2f"|format(event.recovery_time) if event.recovery_time else 'N/A' }}s</p>
        {% if event.error %}
        <p class="error"><strong>Error:</strong> {{ event.error }}</p>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
"""
        template = Template(html_template)
        html_report = template.render(data=data)
        
        with open('chaos_report.html', 'w') as f:
            f.write(html_report)
        logger.info("HTML report generated: chaos_report.html")

    def _check_keyboard(self):
        """Check for keyboard input to skip wait time"""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'n':  # 'n' key pressed
                    logger.info("Skipping wait time...")
                    self.skip_wait = True
            time.sleep(0.1)

    def _wait_with_skip(self, wait_time: float) -> None:
        """Wait for specified time with ability to skip"""
        self.skip_wait = False
        end_time = time.time() + wait_time
        
        while time.time() < end_time and not self.skip_wait:
            remaining = end_time - time.time()
            if remaining > 0:
                logger.info(f"Waiting {remaining:.1f} seconds... (Press 'n' to skip)")
                time.sleep(1)

    def run(self) -> None:
        """Run chaos testing scenarios."""
        logger.info("Starting ChaosCompose testing...")
        logger.info("Press 'n' to skip to next test, Ctrl+C to exit")
        
        # Start keyboard monitoring thread
        keyboard_thread = threading.Thread(target=self._check_keyboard, daemon=True)
        keyboard_thread.start()
        
        end_time = time.time() + (self.config['test_settings']['total_duration_minutes'] * 60)
        
        try:
            while time.time() < end_time:
                for scenario in self.config['scenarios']:
                    self.inject_chaos(scenario)
                    # Wait according to scenario frequency
                    wait_time = scenario['actions'][0]['frequency_minutes'] * 60
                    self._wait_with_skip(wait_time)
                    
        except KeyboardInterrupt:
            logger.info("Testing interrupted by user")
        except Exception as e:
            logger.error(f"Error during testing: {e}")
        finally:
            self.generate_report()
            logger.info("Testing completed")

def main():
    if len(sys.argv) != 2:
        print("Usage: python chaos_compose.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    if not Path(config_file).exists():
        print(f"Config file not found: {config_file}")
        sys.exit(1)

    chaos = ChaosCompose(config_file)
    chaos.run()

if __name__ == "__main__":
    main() 