import paramiko
import logging
from typing import Dict, Any

class SSHConnector:
    def __init__(self, target: str, user: str, password: str = None, key_file: str = None):
        """Initialize SSH connection."""
        self.target = target
        self.user = user
        self.password = password
        self.key_file = key_file
        self.client = None

    def connect(self):
        """Establish SSH connection."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_file:
                private_key = paramiko.RSAKey.from_private_key_file(self.key_file)
                self.client.connect(self.target, username=self.user, pkey=private_key)
            else:
                self.client.connect(self.target, username=self.user, password=self.password)
            
            logging.info(f"Successfully connected to {self.target}")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to {self.target}: {e}")
            return False

    def execute_check(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a compliance check."""
        if not self.client:
            if not self.connect():
                return {'status': 'ERROR', 'error': 'Failed to connect to target'}

        try:
            command = rule.get('command', '')
            stdin, stdout, stderr = self.client.exec_command(command)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if error:
                logging.error(f"Command error: {error}")
                return {'status': 'ERROR', 'error': error}

            expected_output = rule.get('expected_output', '')
            if expected_output and expected_output not in output:
                return {
                    'status': 'FAIL',
                    'output': output,
                    'expected': expected_output
                }
            
            return {'status': 'PASS', 'output': output}

        except Exception as e:
            logging.error(f"Error executing check: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def close(self):
        """Close the SSH connection."""
        if self.client:
            self.client.close()
            logging.info("SSH connection closed")
