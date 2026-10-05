from flask import Flask, render_template, redirect, url_for

from risk_engine import calculate_risk

app = Flask(__name__)


findings = [
    {
        "id": 1,
        "resource": "EC2-Server-01",
        "issue": "SSH port 22 open to the Internet",
        "issue_type": "ssh_open",
        "exposure": "internet",
        "data_sensitivity": "high",
        "recommendation": "Allow SSH only from trusted IP addresses.",
        "status": "Pending Approval"
    },
    {
        "id": 2,
        "resource": "S3-Bucket-01",
        "issue": "S3 bucket is publicly accessible",
        "issue_type": "public_s3",
        "exposure": "internet",
        "data_sensitivity": "high",
        "recommendation": "Block public access to the S3 bucket.",
        "status": "Pending Approval"
    },
    {
        "id": 3,
        "resource": "IAM-User-01",
        "issue": "Excessive IAM permissions",
        "issue_type": "excessive_iam",
        "exposure": "restricted",
        "data_sensitivity": "high",
        "recommendation": "Remove unnecessary permissions.",
        "status": "Pending Approval"
    },
    {
        "id": 4,
        "resource": "Database-01",
        "issue": "Database accessible from the Internet",
        "issue_type": "public_database",
        "exposure": "internet",
        "data_sensitivity": "high",
        "recommendation": "Restrict database access to the application network.",
        "status": "Pending Approval"
    }
]


@app.route("/")
def home():

    total_risk = 0

    for finding in findings:

        score, severity = calculate_risk(
            finding["issue_type"],
            finding["exposure"],
            finding["data_sensitivity"]
        )

        finding["risk"] = score
        finding["severity"] = severity

        total_risk += score

    average_risk = total_risk / len(findings)

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

            finding["status"] = "Remediated"
            finding["verification"] = "Verified"

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)