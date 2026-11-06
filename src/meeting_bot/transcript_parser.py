import re
from typing import List


def normalize_text(text: str) -> str:
    """Clean and normalize meeting transcript text."""
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = cleaned.strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def split_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def extract_lines(text: str) -> List[str]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return lines


def parse_transcript(text: str) -> dict:
    """Render a minimal normalized transcript structure."""
    clean = normalize_text(text)
    sentences = split_sentences(clean)
    lines = extract_lines(clean)
    return {
        "raw": text,
        "clean": clean,
        "sentences": sentences,
        "lines": lines,
    }
