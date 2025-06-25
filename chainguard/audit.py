"""Package auditing functionality."""
import subprocess
import logging

logging.basicConfig(
    filename="chainguard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def audit_package(package_name):
    """Audit a package for vulnerabilities using pip-audit."""
    try:
        # Run pip-audit with plain text output
        result = subprocess.run(
            ["pip-audit", package_name, "--no-deps"],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse plain text output
        output = result.stdout
        vulnerabilities = []
        if "No known vulnerabilities found" in output:
            vulnerabilities = []
        else:
            # Simplified parsing (adjust based on pip-audit output)
            lines = output.splitlines()
            for line in lines:
                if "Vulnerability ID" in line:
                    vulnerabilities.append({"id": line.split(":")[-1].strip()})
        logging.info(f"Audited package {package_name}: {len(vulnerabilities)} vulnerabilities found")
        return {"package": package_name, "vulnerabilities": vulnerabilities}
    except subprocess.CalledProcessError as e:
        logging.error(f"pip-audit failed for {package_name}: {e.stderr}")
        raise Exception(f"Failed to audit package {package_name}: {e.stderr}")
    except Exception as e:
        logging.error(f"Error auditing package {package_name}: {str(e)}")
        raise