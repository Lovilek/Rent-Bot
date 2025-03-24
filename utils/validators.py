import re

def normalize_price(text: str) -> int | None:
    text = re.sub(r"[^\d]", "", text)
    return int(text) if text.isdigit() else None