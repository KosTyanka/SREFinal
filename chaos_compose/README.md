# ChaosCompose

A lightweight chaos testing tool for Docker Compose environments. ChaosCompose helps you test your application's resilience by injecting controlled failures into your services.

## Features

- Automated failure injection for Docker Compose services
- Multiple chaos types:
  - Container kills (SIGTERM/SIGKILL)
  - Container pauses
  - Network delays
- Automatic recovery monitoring
- Prometheus metrics integration
- Detailed HTML and text reports
- Configurable test scenarios

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Running Prometheus and Pushgateway (for metrics)

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a YAML configuration file (e.g., `chaos_config.yaml`) with your test scenarios:

```yaml
# Example configuration
health_check:
  endpoint: "http://localhost:8000/health"
  interval_seconds: 5
  timeout_seconds: 2
  max_retries: 30

scenarios:
  - name: "backend_crash"
    target_service: "backend"
    actions:
      - type: "kill"
        signal: "SIGTERM"
        duration_seconds: 30
        frequency_minutes: 5
```

## Usage

1. Start your Docker Compose services:
```bash
docker-compose up -d
```

2. Run ChaosCompose:
```bash
python chaos_compose.py chaos_config.yaml
```

3. View results:
- Check `chaos_report.txt` and `chaos_report.html` for test results
- Monitor metrics in Prometheus/Grafana

## Test Scenarios

### 1. Service Crash Testing
Tests how your system recovers from sudden service termination:
```yaml
scenarios:
  - name: "backend_crash"
    target_service: "backend"
    actions:
      - type: "kill"
        signal: "SIGTERM"
        duration_seconds: 30
        frequency_minutes: 5
```

### 2. Database Pause Testing
Simulates database freezes:
```yaml
scenarios:
  - name: "database_pause"
    target_service: "db"
    actions:
      - type: "pause"
        duration_seconds: 15
        frequency_minutes: 10
```

### 3. Network Latency Testing
Adds network delays:
```yaml
scenarios:
  - name: "network_delay"
    target_service: "backend"
    actions:
      - type: "network_delay"
        latency_ms: 1000
        duration_seconds: 60
        frequency_minutes: 15
```

## Metrics

ChaosCompose exports the following Prometheus metrics:
- `chaos_test_recovery_time_seconds`: Time taken for service to recover
- `chaos_test_failure_count`: Number of chaos events injected

## Reports

### Text Report
Contains:
- Total number of events
- Successful recoveries
- Average and maximum recovery times
- Detailed event log

### HTML Report
Interactive report with:
- Summary statistics
- Detailed event timeline
- Error highlighting
- Styled presentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License 