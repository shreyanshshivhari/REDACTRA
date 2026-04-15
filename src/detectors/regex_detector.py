import re

PATTERNS = {
    "password": r"(?i)(pass\s*word|pass|pwd)\s*(?:is|=|:)?\s*([^\s]+)",
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
    "api_key": r"(?i)api[_-]?key\s*[:=]?\s*\S+",
    "phone": r"\b\d{10}\b",
    "credential": r"(?i)(login|secret|credential)\s*(?:is|=|:)?\s*([^\s]+)"
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