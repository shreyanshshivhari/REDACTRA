from detectors.regex_detector import detect_sensitive
from detectors.jailbreak_detector import is_jailbreak
from detectors.intent_detector import detect_intent

def analyze_prompt(text):
    result = {
        "sensitive_data": [],
        "jailbreak": False,
        "intent": "safe",
        "action": "allow"
    }

    # Step 1: Sensitive
    sensitive = detect_sensitive(text)
    if sensitive:
        result["sensitive_data"] = sensitive
        result["action"] = "redact"

    # Step 2: Jailbreak
    if is_jailbreak(text):
        result["jailbreak"] = True
        result["action"] = "block"

    # Step 3: Intent
    intent = detect_intent(text)
    result["intent"] = intent

    if intent == "harmful" and not result["jailbreak"]:
        result["action"] = "warn"

    return result