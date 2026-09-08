"""Conservative draft redaction. Not a privacy or security certification."""
import re

RULES = [
    (re.compile(r'-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----.*?-----END (?:[A-Z ]+)?PRIVATE KEY-----', re.S), '[REDACTED PRIVATE KEY]'),
    (re.compile(r'\b(?:sk[-_]|gh[pousr]_|github_pat_|xox[baprs]-|hf_|gsk_|xai-|pplx-|fal_|bb_live_)[A-Za-z0-9_-]{10,}'), '[REDACTED CREDENTIAL]'),
    (re.compile(r'\bAIza[A-Za-z0-9_-]{30,}'), '[REDACTED CREDENTIAL]'),
    (re.compile(r'(?i)Bearer\s+[A-Za-z0-9._~+/=-]+'), 'Bearer [REDACTED]'),
    (re.compile(r'(?i)((?:[A-Z_]*(?:API_KEY|ACCESS_TOKEN|REFRESH_TOKEN|CLIENT_SECRET|PASSWORD|AUTH_TOKEN))[\"\x27]?\s*[:=]\s*)[\"\x27]?[^\s\"\x27,;}]+[\"\x27]?'), r'\1[REDACTED]'),
    (re.compile(r'(?i)([?&](?:api_key|token|access_token|secret|signature)=)[^&\s\"\x27]+'), r'\1[REDACTED]'),
    (re.compile(r'/Users/[^/\s\"\x27]+|/home/[^/\s\"\x27]+'), '<HOME>'),
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), '[IP ADDRESS OMITTED]'),
]

def sanitize(text):
    for pattern, replacement in RULES:
        text = pattern.sub(replacement, text)
    return text
