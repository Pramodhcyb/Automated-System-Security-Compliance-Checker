import subprocess
import logging
from typing import Dict, Any

class LocalConnector:
    def __init__(self):
        """Initialize local connector."""
        self.client = None

    def execute_check(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a compliance check locally."""
        try:
            command = rule.get('command', '')
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                logging.error(f"Command failed with error: {result.stderr}")
                return {
                    'status': 'ERROR',
                    'error': result.stderr
                }

            expected_output = rule.get('expected_output', '')
            if expected_output and expected_output not in result.stdout:
                return {
                    'status': 'FAIL',
                    'output': result.stdout,
                    'expected': expected_output
                }

            return {'status': 'PASS', 'output': result.stdout}

        except subprocess.TimeoutExpired:
            logging.error("Command execution timed out")
            return {'status': 'ERROR', 'error': 'Command timed out'}
        except Exception as e:
            logging.error(f"Error executing check: {e}")
            return {'status': 'ERROR', 'error': str(e)}
