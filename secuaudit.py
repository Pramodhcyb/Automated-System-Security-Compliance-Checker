import argparse
import yaml
import logging
from connectors.ssh_connector import SSHConnector
from connectors.local_connector import LocalConnector
from reporters.text_reporter import TextReporter
from reporters.html_reporter import HTMLReporter

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_rules(rule_file):
    """Load compliance rules from YAML file."""
    try:
        with open(rule_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading rules file: {e}")
        return None

def create_connector(target, user, password=None, key_file=None):
    """Create appropriate connector based on target."""
    if target == 'localhost':
        return LocalConnector()
    return SSHConnector(target, user, password, key_file)

def run_checks(connector, rules):
    """Execute all compliance checks."""
    results = []
    for rule in rules:
        try:
            result = connector.execute_check(rule)
            results.append({
                'rule_id': rule.get('id'),
                'name': rule.get('name'),
                'status': result['status'],
                'actual_output': result.get('output', ''),
                'expected_output': rule.get('expected_output', ''),
                'remediation': rule.get('remediation', '')
            })
        except Exception as e:
            logging.error(f"Error running check {rule.get('id')}: {e}")
            results.append({
                'rule_id': rule.get('id'),
                'name': rule.get('name'),
                'status': 'ERROR',
                'error': str(e)
            })
    return results

def main():
    parser = argparse.ArgumentParser(description='SecuAudit - Automated Security Compliance Checker')
    parser.add_argument('--target', default='localhost', help='Target system to audit')
    parser.add_argument('--user', default='root', help='Username for SSH connection')
    parser.add_argument('--password', help='Password for authentication')
    parser.add_argument('--key-file', help='Path to SSH private key file')
    parser.add_argument('--rules', default='compliance_rules/linux_cis_L1.yaml', help='Path to rules file')
    parser.add_argument('--output-format', choices=['text', 'html'], default='text', help='Output format')
    parser.add_argument('--output-file', help='Path to save output report')

    args = parser.parse_args()

    # Load rules
    rules = load_rules(args.rules)
    if not rules:
        logging.error("Failed to load rules. Exiting.")
        return

    # Create connector
    connector = create_connector(
        args.target,
        args.user,
        args.password,
        args.key_file
    )

    # Run checks
    results = run_checks(connector, rules)

    # Generate report
    if args.output_format == 'html':
        reporter = HTMLReporter()
    else:
        reporter = TextReporter()

    report = reporter.generate_report(results)
    
    # Output to console and optionally to file
    print(report)
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(report)

if __name__ == '__main__':
    main()
