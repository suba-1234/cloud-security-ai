def calculate_risk(finding):

    severity = finding["severity"].lower()
    service = finding["service"].lower()
    issue = finding["issue"].lower()
    description = finding["description"].lower()

    # Base score from Prowler severity
    severity_scores = {
        "critical": 85,
        "high": 70,
        "medium": 50,
        "low": 25
    }

    score = severity_scores.get(severity, 40)

    # Increase risk for important AWS services
    important_services = [
        "iam",
        "s3",
        "ec2",
        "rds",
        "vpc",
        "cloudtrail"
    ]

    if service in important_services:
        score += 5

    # Increase risk for dangerous security conditions
    high_risk_keywords = [
        "public",
        "internet",
        "unauthorized",
        "excessive",
        "privilege",
        "shared role",
        "root",
        "unencrypted",
        "exposed",
        "open",
        "injection"
    ]

    for keyword in high_risk_keywords:
        if keyword in issue or keyword in description:
            score += 5

    # Maximum risk score = 100
    score = min(score, 100)

    # Determine final severity
    if score >= 90:
        final_severity = "Critical"
    elif score >= 70:
        final_severity = "High"
    elif score >= 40:
        final_severity = "Medium"
    else:
        final_severity = "Low"

    return score, final_severity