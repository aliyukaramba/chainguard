"""Unit tests for ChainGuard CLI."""
import pytest
from click.testing import CliRunner
from chainguard.cli import cli

def test_audit_command():
    """Test the audit command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["audit", "--package", "requests"])
    assert result.exit_code == 0
    assert "package" in result.output

def test_report_command():
    """Test the report command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["report", "--package", "requests"])
    assert result.exit_code == 0
    assert "teaRank" in result.output

def test_submit_vuln_command():
    """Test the submit-vuln command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["submit-vuln", "--package", "requests", "--description", "Test vuln"])
    assert result.exit_code == 0
    assert "Submitted vulnerability" in result.output