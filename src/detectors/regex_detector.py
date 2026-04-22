import re

PATTERNS = {
    "password": r"(?i)\b(pass(word)?|pwd)\b\s*(?:is|=|:)?\s*([^\s]+)",

    "email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",

    "api_key": r"(?i)\b(api[\s_-]?key|token|auth[\s_-]?key)\b\s*(?:is|=|:)?\s*([A-Za-z0-9\-_]+)",

    "phone": r"(?:(?:\+91[\-\s]?)?[6-9]\d{9})",

    "otp": r"(?i)\b(otp|one[-\s]?time\s?password)\b\s*(?:is|=|:)?\s*(\d{4,6})",

    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",

    "credential": r"(?i)\b(login|secret|credential)\b\s*(?:is|=|:)?\s*([^\s]+)"
}

def detect_sensitive(text):
    results = []

    for label, pattern in PATTERNS.items():
        matches = re.findall(pattern, text)

        for m in matches:
            if isinstance(m, tuple):
                value = m[-1]   # last group = actual secret
            else:
                value = m

            results.append({
                "type": label,
                "value": value
            })

    return results