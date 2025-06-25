"""Flask-based web dashboard for ChainGuard."""
from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
from chainguard.audit import audit_package
from chainguard.tea_integration import TeaProtocolClient
import logging

# Initialize Flask app and HTTP Basic Auth
app = Flask(__name__)
auth = HTTPBasicAuth()

# Configure logging
logging.basicConfig(
    filename="chainguard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Mock users for basic auth
users = {"admin": "password123"}

@auth.verify_password
def verify_password(username, password):
    """Verify HTTP Basic Auth credentials."""
    return users.get(username) == password

@app.route("/dashboard")
@auth.login_required
def dashboard():
    """Render dashboard with audited packages."""
    try:
        client = TeaProtocolClient()
        packages = ["requests", "flask"]  # Mock package list
        data = []
        for pkg in packages:
            audit_result = audit_package(pkg)
            metadata = client.get_package_metadata(pkg)
            data.append({
                "package": pkg,
                "teaRank": metadata["teaRank"],
                "vulnerabilities": len(audit_result["vulnerabilities"])
            })
        logging.info("Rendered dashboard")
        return render_template("dashboard.html", packages=data)
    except Exception as e:
        logging.error(f"Error rendering dashboard: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/analytics")
@auth.login_required
def analytics():
    """Render dependency graph visualization."""
    try:
        client = TeaProtocolClient()
        package = request.args.get("package", "requests")
        metadata = client.get_package_metadata(package)
        logging.info(f"Rendered analytics for {package}")
        return render_template("analytics.html", package=package, dependencies=metadata["dependencies"])
    except Exception as e:
        logging.error(f"Error rendering analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/submit", methods=["GET", "POST"])
@auth.login_required
def submit_vuln():
    """Handle vulnerability submission form."""
    if request.method == "POST":
        try:
            package = request.form["package"]
            description = request.form["description"]
            client = TeaProtocolClient()
            result = client.submit_vulnerability(package, description)
            logging.info(f"Submitted vulnerability via web for {package}")
            return jsonify({"message": result})
        except Exception as e:
            logging.error(f"Error submitting vulnerability via web: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return render_template("submit.html")

if __name__ == "__main__":
    app.run(debug=True)