import requests
import re

# Direct link to TypeScript Book main README (raw markdown)
TS_BOOK_RAW_URL = "https://raw.githubusercontent.com/basarat/typescript-book/master/README.md"

def load_documents():
    try:
        print("Fetching TypeScript Book content from GitHub...")
        text = requests.get(TS_BOOK_RAW_URL, timeout=10).text
        return [("typescript-book/README.md", text)]
    except Exception as e:
        print("Error loading remote doc:", e)
        return []

def find_best_snippet(query: str, docs):
    q_tokens = [t.lower() for t in re.findall(r"\w+|!!|=>", query)]
    best_score, best_snippet, best_source = 0, "", ""
    for path, text in docs:
        text_low = text.lower()
        score = sum(text_low.count(tok) for tok in q_tokens if tok)
        if score > best_score:
            best_score = score
            for tok in q_tokens:
                pos = text_low.find(tok)
                if pos != -1:
                    start, end = max(0, pos - 120), min(len(text), pos + 240)
                    snippet = text[start:end].strip()
                    best_snippet = snippet.replace("\n", " ")
                    best_source = path
                    break
    return best_snippet, best_source

DOCS = load_documents()
