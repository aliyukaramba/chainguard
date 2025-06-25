"""Command-line interface for ChainGuard using Click."""
import click
import json
import logging
from .audit import audit_package
from .tea_integration import TeaProtocolClient

# Configure logging
logging.basicConfig(
    filename="chainguard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose logging")
def cli(verbose):
    """ChainGuard CLI for dependency auditing and Tea Protocol integration."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

@cli.command()
@click.option('--package', required=True, help="Name of the PyPI package to audit")
def audit(package):
    """Audit a PyPI package for vulnerabilities using pip-audit."""
    try:
        result = audit_package(package)
        click.echo(json.dumps(result, indent=2))
        logging.info(f"Audited package: {package}")
    except Exception as e:
        logging.error(f"Error auditing package {package}: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--package', required=True, help="Name of the package to generate report for")
def report(package):
    """Fetch package teaRank and dependency graph from Tea Protocol."""
    try:
        client = TeaProtocolClient()
        metadata = client.get_package_metadata(package)
        click.echo(json.dumps(metadata, indent=2))
        logging.info(f"Generated report for package: {package}")
    except Exception as e:
        logging.error(f"Error generating report for {package}: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--package', required=True, help="Name of the package with vulnerability")
@click.option('--description', required=True, help="Description of the vulnerability")
def submit_vuln(package, description):
    """Submit a vulnerability report with TEA token staking."""
    try:
        client = TeaProtocolClient()
        result = client.submit_vulnerability(package, description)
        click.echo(f"Vulnerability submitted: {result}")
        logging.info(f"Submitted vulnerability for {package}")
    except Exception as e:
        logging.error(f"Error submitting vulnerability for {package}: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    cli()