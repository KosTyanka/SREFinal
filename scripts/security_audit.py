#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import requests
from datetime import datetime

class SecurityAuditor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'findings': [],
            'summary': {
                'high': 0,
                'medium': 0,
                'low': 0
            }
        }

    def add_finding(self, severity, category, description, recommendation):
        finding = {
            'severity': severity,
            'category': category,
            'description': description,
            'recommendation': recommendation
        }
        self.report['findings'].append(finding)
        self.report['summary'][severity] += 1

    def check_docker_security(self):
        """Check Docker container security configuration"""
        try:
            # Check if containers are running as non-root
            containers = subprocess.check_output(['docker', 'ps', '--format', '{{.Names}}'])
            for container in containers.decode().split('\n'):
                if not container:
                    continue
                user = subprocess.check_output(
                    ['docker', 'inspect', '--format', '{{.Config.User}}', container]
                ).decode().strip()
                
                if not user:
                    self.add_finding(
                        'high',
                        'Container Security',
                        f'Container {container} is running as root',
                        'Configure container to run as non-root user'
                    )

            # Check if containers have resource limits
            for container in containers.decode().split('\n'):
                if not container:
                    continue
                limits = subprocess.check_output(
                    ['docker', 'inspect', '--format', '{{.HostConfig.Resources}}', container]
                ).decode()
                
                if '"Memory":0' in limits:
                    self.add_finding(
                        'medium',
                        'Resource Management',
                        f'Container {container} has no memory limit',
                        'Set appropriate memory limits for containers'
                    )

        except subprocess.CalledProcessError as e:
            print(f"Error checking Docker security: {e}")

    def check_api_security(self):
        """Check API endpoint security"""
        try:
            # Check CORS configuration
            headers = requests.options(f"{self.base_url}/concerts").headers
            if '*' in headers.get('Access-Control-Allow-Origin', ''):
                self.add_finding(
                    'medium',
                    'API Security',
                    'CORS is configured to allow all origins (*)',
                    'Restrict CORS to specific trusted origins'
                )

            # Check for security headers
            response = requests.get(f"{self.base_url}/health")
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block'
            }
            
            for header, expected in security_headers.items():
                if header not in response.headers:
                    self.add_finding(
                        'medium',
                        'HTTP Security',
                        f'Missing security header: {header}',
                        f'Add {header} header with value: {expected}'
                    )

        except requests.exceptions.RequestException as e:
            print(f"Error checking API security: {e}")

    def check_dependencies(self):
        """Check for known vulnerabilities in dependencies"""
        try:
            # Check Python dependencies
            if os.path.exists('backend/requirements.txt'):
                result = subprocess.run(
                    ['safety', 'check', '-r', 'backend/requirements.txt'],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    self.add_finding(
                        'high',
                        'Dependencies',
                        'Vulnerable Python dependencies found',
                        'Update dependencies to secure versions'
                    )

            # Check npm dependencies
            if os.path.exists('frontend/package.json'):
                result = subprocess.run(
                    ['npm', 'audit', '--json'],
                    cwd='frontend',
                    capture_output=True,
                    text=True
                )
                audit_result = json.loads(result.stdout)
                if audit_result.get('vulnerabilities', {}):
                    self.add_finding(
                        'high',
                        'Dependencies',
                        'Vulnerable npm packages found',
                        'Run npm audit fix to update vulnerable packages'
                    )

        except subprocess.CalledProcessError as e:
            print(f"Error checking dependencies: {e}")

    def check_database_security(self):
        """Check database security configuration"""
        try:
            # Check if Postgres is exposed publicly
            netstat = subprocess.check_output(['netstat', '-tuln']).decode()
            if ':5432' in netstat and '0.0.0.0:5432' in netstat:
                self.add_finding(
                    'high',
                    'Database Security',
                    'PostgreSQL is exposed on all interfaces',
                    'Restrict PostgreSQL to listen only on necessary interfaces'
                )

        except subprocess.CalledProcessError as e:
            print(f"Error checking database security: {e}")

    def run_audit(self):
        """Run all security checks"""
        print("Starting security audit...")
        
        self.check_docker_security()
        self.check_api_security()
        self.check_dependencies()
        self.check_database_security()
        
        return self.generate_report()

    def generate_report(self):
        """Generate a formatted security report"""
        report_str = "\nSecurity Audit Report\n"
        report_str += "===================\n\n"
        
        report_str += "Summary:\n"
        report_str += f"High severity issues: {self.report['summary']['high']}\n"
        report_str += f"Medium severity issues: {self.report['summary']['medium']}\n"
        report_str += f"Low severity issues: {self.report['summary']['low']}\n\n"
        
        report_str += "Detailed Findings:\n"
        for finding in self.report['findings']:
            report_str += f"\n[{finding['severity'].upper()}] {finding['category']}\n"
            report_str += f"Description: {finding['description']}\n"
            report_str += f"Recommendation: {finding['recommendation']}\n"
        
        return report_str

def main():
    if len(sys.argv) < 2:
        print("Usage: security_audit.py <base_url>")
        sys.exit(1)

    base_url = sys.argv[1]
    auditor = SecurityAuditor(base_url)
    report = auditor.run_audit()
    
    print(report)
    
    # Save report to file
    with open('security_audit_report.txt', 'w') as f:
        f.write(report)

if __name__ == '__main__':
    main() 