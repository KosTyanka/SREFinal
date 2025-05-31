import subprocess
import json
import time
import requests
import threading
import argparse
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class TicketLoadTester:
    def __init__(self, base_url, pushgateway_url):
        self.base_url = base_url
        self.pushgateway_url = pushgateway_url
        self.registry = CollectorRegistry()
        
        # Custom metrics
        self.current_rps = Gauge('load_test_current_rps', 'Current requests per second',
                               registry=self.registry)
        self.error_rate = Gauge('load_test_error_rate', 'Error rate percentage',
                              registry=self.registry)
        self.p95_latency = Gauge('load_test_p95_latency', '95th percentile latency',
                                registry=self.registry)

    def run_ab_test(self, concurrency, total_requests, endpoint, data=None):
        """Run Apache Bench test with specified parameters"""
        if data:
            with open('test_data.json', 'w') as f:
                json.dump(data, f)
            ab_cmd = [
                'ab', '-c', str(concurrency), '-n', str(total_requests),
                '-p', 'test_data.json', '-T', 'application/json',
                f'{self.base_url}{endpoint}'
            ]
        else:
            ab_cmd = [
                'ab', '-c', str(concurrency), '-n', str(total_requests),
                f'{self.base_url}{endpoint}'
            ]

        try:
            result = subprocess.run(ab_cmd, capture_output=True, text=True)
            return self.parse_ab_output(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running ab: {e}")
            return None

    def parse_ab_output(self, output):
        """Parse Apache Bench output and extract key metrics"""
        metrics = {}
        for line in output.split('\n'):
            if 'Requests per second' in line:
                metrics['rps'] = float(line.split(':')[1].strip().split(' ')[0])
            elif 'Failed requests' in line:
                metrics['failed_requests'] = int(line.split(':')[1].strip())
            elif '95%' in line:
                metrics['p95_latency'] = float(line.strip().split()[1])
        return metrics

    def push_metrics(self, metrics):
        """Push metrics to Prometheus Pushgateway"""
        self.current_rps.set(metrics['rps'])
        self.error_rate.set(metrics['failed_requests'])
        self.p95_latency.set(metrics['p95_latency'])
        
        try:
            push_to_gateway(self.pushgateway_url, job='load_test', registry=self.registry)
        except Exception as e:
            print(f"Error pushing to Pushgateway: {e}")

    def run_purchase_test(self, concert_id, concurrency=10, requests=100):
        """Test concurrent ticket purchases"""
        data = {
            "concert_id": concert_id,
            "quantity": 1
        }
        
        print(f"Running purchase test with {concurrency} concurrent users...")
        metrics = self.run_ab_test(concurrency, requests, '/purchase', data)
        
        if metrics:
            print(f"Results:")
            print(f"Requests per second: {metrics['rps']}")
            print(f"Failed requests: {metrics['failed_requests']}")
            print(f"95th percentile latency: {metrics['p95_latency']} ms")
            
            self.push_metrics(metrics)
        
        return metrics

    def run_gradual_load_test(self, max_concurrency, step=10, duration=60):
        """Gradually increase load and monitor system behavior"""
        print(f"Running gradual load test up to {max_concurrency} concurrent users...")
        
        for concurrency in range(step, max_concurrency + step, step):
            print(f"\nTesting with {concurrency} concurrent users...")
            metrics = self.run_purchase_test(1, concurrency, concurrency * 10)
            
            if metrics and metrics['failed_requests'] > concurrency * 10 * 0.1:
                print(f"High error rate detected at {concurrency} users. Stopping test.")
                break
            
            time.sleep(5)  # Cool down between tests

def main():
    parser = argparse.ArgumentParser(description='Concert Ticketing Load Tester')
    parser.add_argument('--url', default='http://localhost:8000',
                       help='Base URL of the ticketing service')
    parser.add_argument('--pushgateway', default='http://localhost:9091',
                       help='Prometheus Pushgateway URL')
    parser.add_argument('--max-users', type=int, default=100,
                       help='Maximum number of concurrent users')
    args = parser.parse_args()

    tester = TicketLoadTester(args.url, args.pushgateway)
    
    # Create a test concert if needed
    try:
        response = requests.post(f"{args.url}/concerts", json={
            "name": "Load Test Concert",
            "date": "2024-01-01T20:00:00",
            "venue": "Test Venue",
            "total_tickets": 10000
        })
        concert_id = response.json()['id']
    except Exception as e:
        print(f"Error creating test concert: {e}")
        return

    # Run gradual load test
    tester.run_gradual_load_test(args.max_users)

if __name__ == '__main__':
    main() 