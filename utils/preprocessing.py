import re

def clean_text(text: str) -> str:
    """Cleans and normalizes input text."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)         # Collapse whitespace
    text = re.sub(r'[^\w\s?.!,\'"-]', '', text)  # Remove unusual chars
    return text


def tokenize(text: str) -> list:
    return re.findall(r'\b\w+\b', text.lower())


def truncate(text: str, max_chars: int = 2000) -> str:
    return text[:max_chars] + "..." if len(text) > max_chars else text