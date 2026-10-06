def generate_explanation(finding):

    issue = finding["issue"].lower()
    service = finding["service"].lower()
    severity = finding["severity"]

    if "logging" in issue or "cloudtrail" in issue:
        explanation = (
            "Logging is important for detecting suspicious activity "
            "and investigating security incidents. Without proper "
            "logging, unauthorized actions may be difficult to trace."
        )

    elif "public" in issue or "internet" in issue or "exposed" in issue:
        explanation = (
            "The resource may be accessible from the public internet. "
            "This increases the possibility of unauthorized access, "
            "data exposure, or malicious activity."
        )

    elif "iam" in service or "permission" in issue or "role" in issue:
        explanation = (
            "Excessive or incorrectly configured permissions can allow "
            "users or services to access resources beyond what they need. "
            "This violates the principle of least privilege."
        )

    elif "encryption" in issue or "encrypted" in issue:
        explanation = (
            "The resource may not have sufficient encryption protection. "
            "If sensitive data is exposed, encryption helps reduce the "
            "impact of unauthorized access."
        )

    elif "guardrail" in issue:
        explanation = (
            "Security guardrails help control unsafe or unwanted AI "
            "model interactions. Missing or incomplete guardrails can "
            "increase the risk of unsafe model usage."
        )

    elif "root" in issue:
        explanation = (
            "The AWS root account has highly privileged access. "
            "Incorrect root-account security can have a major impact "
            "because the account can perform sensitive AWS operations."
        )

    else:
        explanation = (
            "This configuration does not follow recommended cloud "
            "security practices and may increase the risk of "
            "unauthorized access or security incidents."
        )

    return explanation