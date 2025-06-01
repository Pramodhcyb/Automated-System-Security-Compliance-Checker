# SecuAudit - Automated Security Compliance Checker

SecuAudit is an automated security compliance checking tool that verifies system configurations against predefined security benchmarks and best practices. It can be used to audit Linux servers, Windows machines, and specific applications for security compliance.

## Features

- Automated compliance checking against predefined rules
- Support for both local and remote system auditing via SSH
- Multiple output formats (text, HTML)
- Detailed reporting with pass/fail status and remediation steps
- Configurable rules using YAML format
- Rich console output with color-coded results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pramodhcyb/Automated-System-Security-Compliance-Checker
cd secuaudit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Installation
First, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Basic Usage
The tool can be used in several ways depending on your needs:

#### Local System Audit
To audit the local system:
```bash
python secuaudit.py --target localhost
```

#### Remote System Audit
For remote systems, use appropriate credentials:

##### Linux Remote System
```bash
# Using SSH key authentication
python secuaudit.py \
    --target remote-linux-host \
    --user admin \
    --key-file ~/.ssh/id_rsa \
    --rules compliance_rules/linux_cis_L1.yaml

# Using password authentication
python secuaudit.py \
    --target remote-linux-host \
    --user admin \
    --password your_password \
    --rules compliance_rules/linux_cis_L1.yaml
```

##### Windows Remote System
```bash
python secuaudit.py \
    --target remote-windows-host \
    --user administrator \
    --password your_password \
    --rules compliance_rules/windows_cis_L1.yaml
```

### 3. Output Formats
The tool supports multiple output formats:

#### Text Output (Console)
```bash
python secuaudit.py --output-format text
```

#### HTML Report
```bash
python secuaudit.py \
    --output-format html \
    --output-file audit-report.html
```

#### CSV Format
```bash
python secuaudit.py \
    --output-format csv \
    --output-file audit-report.csv
```

### 4. Common Options
- `--target`: Target system to audit (localhost or remote hostname/IP)
- `--user`: Username for authentication
- `--password`: Password for authentication (use with caution)
- `--key-file`: Path to SSH private key file (for Linux)
- `--rules`: Path to rules file (default: compliance_rules/linux_cis_L1.yaml)
- `--output-format`: Report format (text/html/csv)
- `--output-file`: Path to save the report file

### 5. Example Scenarios

#### Local Windows Audit
```bash
python secuaudit.py \
    --target localhost \
    --rules compliance_rules/windows_cis_L1.yaml \
    --output-format html \
    --output-file windows-audit.html
```

#### Remote Linux Audit with SSH Key
```bash
python secuaudit.py \
    --target 192.168.1.100 \
    --user admin \
    --key-file ~/.ssh/id_rsa \
    --rules compliance_rules/linux_cis_L1.yaml \
    --output-format html \
    --output-file linux-audit.html
```

#### Multiple Rule Sets
You can specify multiple rule files:
```bash
python secuaudit.py \
    --target localhost \
    --rules compliance_rules/windows_cis_L1.yaml \
    --rules compliance_rules/custom_rules.yaml
```

### 6. Best Practices
1. Always use SSH key authentication for Linux systems when possible
2. Store credentials securely (consider using environment variables)
3. Run audits during maintenance windows if possible
4. Keep rules files version controlled
5. Regularly update rules to match latest security standards

### 7. Troubleshooting

#### Common Errors
- **SSH Connection Failed**: Check SSH service status and firewall rules
- **Authentication Failed**: Verify credentials and permissions
- **Command Execution Failed**: Ensure target system has required tools installed
- **Permission Denied**: Run with appropriate privileges

#### Debugging
Add `--debug` flag for detailed logging:
```bash
python secuaudit.py --target localhost --debug
```

## Rule Configuration
Rules are defined in YAML files. Each rule contains:
- id: Unique identifier
- name: Human-readable name
- platform: Target platform (linux/windows/general)
- command: Command to execute
- expected_output: Expected output pattern
- severity: High/Medium/Low
- remediation: Steps to fix non-compliant settings

### Linux Rules Example
```yaml
rules:
  - id: CIS-L1-001
    name: "Ensure SSH Root Login is Disabled"
    platform: linux
    command: "grep '^PermitRootLogin' /etc/ssh/sshd_config"
    expected_output: "PermitRootLogin no"
    severity: high
    remediation: "Edit /etc/ssh/sshd_config and set PermitRootLogin to no"
```

### Windows Rules Example
```yaml
rules:
  - id: CIS-W1-001
    name: "Ensure Windows Firewall is Enabled"
    platform: windows
    command: "powershell -Command 'Get-NetFirewallProfile | Select-Object Name,Enabled | Format-List'"
    expected_output: "Enabled : True"
    severity: high
    remediation: "Enable Windows Firewall through Windows Security settings or run 'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True'"

  - id: CIS-W1-002
    name: "Check Windows Update Status"
    platform: windows
    command: "powershell -Command 'Get-WindowsUpdateLog | Select-Object -Last 1'"
    expected_output: "Installed"
    severity: high
    remediation: "Run Windows Update to install pending updates"

  - id: CIS-W1-003
    name: "Check Remote Desktop Access"
    platform: windows
    command: "powershell -Command 'Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" | Select-Object -ExpandProperty fDenyTSConnections'"
    expected_output: "1"
    severity: high
    remediation: "Disable Remote Desktop if not needed or configure it securely"

  - id: CIS-W1-004
    name: "Check User Account Control (UAC)"
    platform: windows
    command: "powershell -Command 'Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA" | Select-Object -ExpandProperty EnableLUA'"
    expected_output: "1"
    severity: high
    remediation: "Enable UAC through Windows Security settings"

  - id: CIS-W1-005
    name: "Check Windows Defender Status"
    platform: windows
    command: "powershell -Command 'Get-MpComputerStatus | Select-Object AMServiceEnabled,AntivirusEnabled,AntispywareEnabled'"
    expected_output: "AMServiceEnabled : True\nAntivirusEnabled : True\nAntispywareEnabled : True"
    severity: high
    remediation: "Enable Windows Defender through Windows Security settings"
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
