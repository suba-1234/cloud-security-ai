import pandas as pd
import glob

from risk_engine import calculate_risk
from ai_explainer import generate_explanation


def load_prowler_findings():

    files = glob.glob("output/*.csv")

    if not files:
        return []

    csv_file = files[0]

    df = pd.read_csv(csv_file, sep=";")

    # Only failed security findings
    df = df[df["STATUS"] == "FAIL"]

    findings = []

    for index, row in df.iterrows():

        finding = {
    "id": len(findings) + 1,
    "check_id": str(row["CHECK_ID"]),
    "resource_uid": str(row["RESOURCE_UID"]),
    "resource": str(row["RESOURCE_NAME"]),
    "service": str(row["SERVICE_NAME"]),
    "issue": str(row["CHECK_TITLE"]),
    "severity": str(row["SEVERITY"]).capitalize(),
    "risk": 0,
    "description": str(row["DESCRIPTION"]),
    "recommendation": str(
        row["REMEDIATION_RECOMMENDATION_TEXT"]
    ),
    "status": "Pending Approval",
    "verification": "",
    "ai_explanation": ""
}

        risk_score, final_severity = calculate_risk(finding)

        finding["risk"] = risk_score
        finding["severity"] = final_severity
        finding["ai_explanation"]=generate_explanation(finding)

        findings.append(finding)

    return findings