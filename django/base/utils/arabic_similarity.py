import re
from difflib import SequenceMatcher

# regex dasar
WAQF = set("ۚۛۗۙۖۘۢ")
DIACRITIC_RE = re.compile(r"[\u064B-\u0652\u0670\u0653-\u0655]")  # harakat
TATWEEL_RE = re.compile(r"\u0640")  # tatweel/kashida
WAQF_RE = re.compile(rf"[{''.join(WAQF)}]")


def normalize_arabic(s: str) -> str:
    if not s:
        return ""
    s2 = s
    s2 = WAQF_RE.sub("", s2)  # buang waqaf
    s2 = TATWEEL_RE.sub("", s2)  # buang tatweel
    s2 = DIACRITIC_RE.sub("", s2)  # buang harakat
    s2 = s2.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ٱ", "ا")
    s2 = s2.replace("ى", "ي")  # unify ya
    s2 = s2.replace("ة", "ه")  # optional ta marbuta
    s2 = s2.replace("ﻻ", "لا")  # ligature laam-alif
    return s2


def similarity_score(a: str, b: str) -> float:
    """Skor similarity 0..100 (pakai SequenceMatcher)"""
    na, nb = normalize_arabic(a), normalize_arabic(b)
    return SequenceMatcher(None, na, nb).ratio() * 100


def is_similar(a: str, b: str, threshold: int = 90) -> bool:
    return similarity_score(a, b) >= threshold
