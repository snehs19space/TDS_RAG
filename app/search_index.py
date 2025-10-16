import os
import re
from pathlib import Path
from typing import List, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "typescript-book"

def load_documents() -> List[Tuple[str, str]]:
    """
    Load all .md, .markdown, .txt, .html files under data/typescript-book.
    Returns list of (relative_path, content).
    """
    docs = []
    if not DATA_DIR.exists():
        return docs
    for p in DATA_DIR.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".markdown", ".txt", ".html"}:
            text = p.read_text(encoding="utf-8", errors="ignore")
            docs.append((str(p.relative_to(DATA_DIR.parent)), text))
    return docs

def find_best_snippet(query: str, docs: List[Tuple[str, str]]) -> Tuple[str, str]:
    """
    Very light-weight scoring: token match count. Return (snippet, source_path).
    """
    q_tokens = [t.lower() for t in re.findall(r"\w+|!!|=>", query)]
    best_score = 0
    best_snippet = ""
    best_source = ""
    for path, text in docs:
        text_low = text.lower()
        score = sum(text_low.count(tok) for tok in q_tokens if tok)
        if score > best_score:
            best_score = score
            # extract a short snippet around first occurrence of most common token
            for tok in q_tokens:
                pos = text_low.find(tok)
                if pos != -1:
                    start = max(0, pos - 120)
                    end = min(len(text), pos + 240)
                    snippet = text[start:end].strip()
                    best_snippet = snippet.replace("\n", " ")
                    best_source = path
                    break
    return best_snippet, best_source

# Preload docs (module-level)
DOCS = load_documents()
