from flask import Flask, render_template, redirect, url_for
from prowler_parser import load_prowler_findings
from remediation import remediate_finding
app = Flask(__name__)

findings = load_prowler_findings()


@app.route("/")
def home():

    total_risk = 0

    for finding in findings:
        total_risk += finding["risk"]

    if len(findings) > 0:
        average_risk = total_risk / len(findings)
    else:
        average_risk = 0

    health_score = round(100 - average_risk)

    return render_template(
        "dashboard.html",
        findings=findings,
        health_score=health_score
    )


@app.route("/approve/<int:finding_id>")
def approve(finding_id):

    for finding in findings:

        if finding["id"] == finding_id:

            result = remediate_finding(finding)

            if result["success"]:
                finding["status"] = "Remediated"
                finding["verification"] = "Pending Re-scan"
                finding["remediation_message"] = result["message"]

            else:
                finding["status"] = "Remediation Pending"
                finding["verification"] = "Not Verified"
                finding["remediation_message"] = result["message"]

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)