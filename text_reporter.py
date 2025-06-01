from rich.console import Console
from rich.table import Table
from typing import List, Dict

class TextReporter:
    def __init__(self):
        self.console = Console()

    def generate_report(self, results: List[Dict]) -> str:
        """Generate a text-based report using Rich for formatting."""
        table = Table(title="Security Compliance Report")
        
        # Add columns
        table.add_column("Rule ID", style="cyan")
        table.add_column("Check Name", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Details")

        # Counters for statistics
        pass_count = 0
        fail_count = 0
        error_count = 0

        # Add rows to table
        for result in results:
            status = result['status']
            if status == 'PASS':
                pass_count += 1
                status_style = "green"
            elif status == 'FAIL':
                fail_count += 1
                status_style = "red"
            else:
                error_count += 1
                status_style = "yellow"

            table.add_row(
                result.get('rule_id', ''),
                result.get('name', ''),
                f"[{status_style}]{status}[/{status_style}]",
                self._format_details(result)
            )

        # Add summary
        table.add_row(
            "",
            "",
            f"Total: {len(results)} | Pass: {pass_count} | Fail: {fail_count} | Error: {error_count}",
            ""
        )

        # Generate report as string
        with self.console.capture() as capture:
            self.console.print(table)
        return capture.get() + "\n"

    def _format_details(self, result: Dict) -> str:
        """Format the details section of the report."""
        if result['status'] == 'ERROR':
            return f"Error: {result.get('error', '')}"
        if result['status'] == 'FAIL':
            return f"Expected: {result.get('expected_output', '')}\nFound: {result.get('actual_output', '')}"
        return ""

    def save_to_file(self, report: str, filename: str):
        """Save report to a file."""
        with open(filename, 'w') as f:
            f.write(report)
