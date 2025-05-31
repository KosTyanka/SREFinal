# High-Load Concert Ticketing Service

A scalable concert ticketing system designed to handle high-load scenarios with SRE best practices.

## Features
- View available concerts and ticket availability
- Purchase tickets with concurrency control
- Real-time monitoring and alerting
- Secure and scalable infrastructure
- Load testing capabilities

## Architecture
- Frontend: React.js
- Backend: Python FastAPI
- Database: PostgreSQL
- Infrastructure: Docker + Terraform
- Monitoring: Prometheus + Grafana

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- Terraform 1.0+

### Local Development Setup
1. Clone the repository
2. Run `docker-compose up` to start all services
3. Access the application at http://localhost:3000

### Production Deployment
See [deployment documentation](./docs/deployment.md) for production setup instructions.

## Documentation
- [Architecture Overview](./docs/architecture.md)
- [Development Guide](./docs/development.md)
- [Monitoring Setup](./docs/monitoring.md)
- [Security Guidelines](./docs/security.md)
- [Load Testing](./docs/load-testing.md)

## Contributing
Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and development process.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 