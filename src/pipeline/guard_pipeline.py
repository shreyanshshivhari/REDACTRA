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

    # Step 1: Run all detectors first
    sensitive = detect_sensitive(text)
    jailbreak = is_jailbreak(text)
    intent = detect_intent(text)

    # Store results
    result["sensitive_data"] = sensitive
    result["jailbreak"] = jailbreak
    result["intent"] = intent

    # Step 2: Decision logic (PRIORITY BASED)
    if sensitive:
        result["action"] = "block"   # or "redact" if you prefer
    elif jailbreak:
        result["action"] = "block"
    elif intent == "harmful":
        result["action"] = "warn"
    else:
        result["action"] = "allow"

    return result