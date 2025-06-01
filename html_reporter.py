from typing import List, Dict
from datetime import datetime

class HTMLReporter:
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Compliance Report</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .report-header { padding: 20px; background: #f5f5f5; }
        .report-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .report-table th, .report-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .report-table th { background-color: #4CAF50; color: white; }
        .pass { background-color: #d4edda; color: #155724; }
        .fail { background-color: #f8d7da; color: #721c24; }
        .error { background-color: #fff3cd; color: #856404; }
        .summary { background-color: #f8f9fa; padding: 15px; }
    </style>
</head>
<body>
    <div class="report-header">
        <h1>Security Compliance Report</h1>
        <p>Generated on: {date}</p>
    </div>

    <table class="report-table">
        <thead>
            <tr>
                <th>Rule ID</th>
                <th>Check Name</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
{rows}
        </tbody>
    </table>

    <div class="summary">
        <h2>Summary</h2>
        <p>Total Checks: {total}</p>
        <p>Passed: {passed}</p>
        <p>Failed: {failed}</p>
        <p>Errors: {errors}</p>
    </div>
</body>
</html>
"""

    def generate_report(self, results: List[Dict]) -> str:
        """Generate an HTML report."""
        # Count statistics
        pass_count = sum(1 for r in results if r['status'] == 'PASS')
        fail_count = sum(1 for r in results if r['status'] == 'FAIL')
        error_count = sum(1 for r in results if r['status'] == 'ERROR')

        # Generate table rows
        rows = ""
        for result in results:
            status = result['status']
            status_class = status.lower()
            
            rows += f"""
            <tr class="{status_class}">
                <td>{result.get('rule_id', '')}</td>
                <td>{result.get('name', '')}</td>
                <td>{status}</td>
                <td>{self._format_details(result)}</td>
            </tr>
            """

        # Format the template
        return self.template.format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            rows=rows,
            total=len(results),
            passed=pass_count,
            failed=fail_count,
            errors=error_count
        )

    def _format_details(self, result: Dict) -> str:
        """Format the details section of the report."""
        if result['status'] == 'ERROR':
            return f"<strong>Error:</strong> {result.get('error', '')}"
        if result['status'] == 'FAIL':
            return f"""
            <strong>Expected:</strong> {result.get('expected_output', '')}<br>
            <strong>Found:</strong> {result.get('actual_output', '')}
            """
        return ""
