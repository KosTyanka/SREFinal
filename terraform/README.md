# Concert Ticketing System Infrastructure

This directory contains the Terraform configuration for deploying the Concert Ticketing System infrastructure on AWS.

## Architecture

The infrastructure consists of:
- VPC with public subnets across multiple availability zones
- ECS Fargate cluster for running containerized applications
- ECR repositories for storing container images
- RDS PostgreSQL instance for the database
- Application Load Balancer for routing traffic
- Security groups for controlling access

## Prerequisites

1. AWS CLI installed and configured
2. Terraform installed (version ~> 1.0)
3. Docker installed (for building and pushing container images)

## Configuration Setup

### Option 1: Using terraform.tfvars (Recommended)

1. Copy the template file:
   ```bash
   cp terraform.tfvars.template terraform.tfvars
   ```

2. Edit `terraform.tfvars` and fill in your values:
   ```hcl
   aws_region = "your-region"
   vpc_cidr = "your-vpc-cidr"
   availability_zones = ["zone-1", "zone-2"]
   db_username = "your-db-username"
   db_password = "your-db-password"
   ```

### Option 2: Using Environment Variables

If you prefer using environment variables, you can set them directly:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export TF_VAR_db_username="your-db-username"
export TF_VAR_db_password="your-db-password"
```

## Deployment Instructions

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Review the Terraform plan:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

## Infrastructure Components

### Networking
- VPC with CIDR block 10.0.0.0/16
- Public subnets in multiple availability zones
- Internet Gateway for public internet access
- Route tables for subnet routing

### Compute
- ECS Fargate cluster
- Frontend service (2 tasks)
- Backend service (2 tasks)
- ECR repositories for container images

### Database
- RDS PostgreSQL instance
- DB subnet group
- Security group for database access

### Load Balancing
- Application Load Balancer
- Target groups for frontend and backend services
- Listener rules for routing traffic

## Security

- Security groups restrict access to necessary ports only
- RDS instance accessible only from ECS tasks
- ALB exposed to internet on port 80 only
- Sensitive variables should be stored securely and never committed to version control

## Outputs

After applying the configuration, you'll get:
- ALB DNS name for accessing the application
- ECR repository URLs for pushing container images
- RDS endpoint for database connections
- ECS cluster name

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

## Important Notes

- The infrastructure is designed for a production environment
- High availability is ensured through multiple AZs
- Auto-scaling can be configured based on needs
- Costs will be incurred for running these resources
- Never commit `terraform.tfvars` or any files containing sensitive information to version control
- Add `*.tfvars` to your `.gitignore` file 