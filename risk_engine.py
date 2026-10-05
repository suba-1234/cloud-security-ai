def calculate_risk(issue_type, exposure, data_sensitivity):
    score = 0

    # Issue severity
    issue_scores = {
        "ssh_open": 30,
        "public_s3": 40,
        "excessive_iam": 25,
        "public_database": 40
    }

    # Internet exposure
    exposure_scores = {
        "internet": 30,
        "restricted": 10
    }

    # Data sensitivity
    sensitivity_scores = {
        "high": 30,
        "medium": 20,
        "low": 10
    }

    score += issue_scores.get(issue_type, 10)
    score += exposure_scores.get(exposure, 10)
    score += sensitivity_scores.get(data_sensitivity, 10)

    if score >= 90:
        severity = "Critical"
    elif score >= 70:
        severity = "High"
    elif score >= 40:
        severity = "Medium"
    else:
        severity = "Low"

    return score, severity
