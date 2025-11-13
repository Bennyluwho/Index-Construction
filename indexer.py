
#TODO: Number of unique tokens
#TODO: Total size (in KB) of your index on disk
#TODO: OPTIONAL save the time it takes

from bs4 import BeautifulSoup
import json
from pathlib import Path
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from collections import defaultdict
import time


#Number of indexed documents
tokenizer = RegexpTokenizer(r"\w+")
ps = PorterStemmer()
inverted_index = defaultdict(set)
doc_id_to_url = []      
root = Path("analyst")


def tokenize_and_stem_unique(text: str) -> set[str]:
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t.isalpha()]
    stems = { ps.stem(t) for t in tokens }  # set → unique stems
    return stems

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

def index_document(doc_id: int, html: str, index):
    text = extract_text(html)
    stemmed_tokens = tokenize_and_stem_unique(text)

    for token in stemmed_tokens:
        index[token].add(doc_id)

def save_index_to_disk(inverted_index, filename="inverted_index.json") -> None:
    serializable_index = { token: list(doc_ids) for token, doc_ids in inverted_index.items() }

    index_path = Path(filename)
    with index_path.open("w", encoding="utf-8") as f:
        json.dump(serializable_index, f)

def save_docs_to_disk(doc_id_to_url, filename="docs.json") -> None:
    docs_path = Path(filename)
    with docs_path.open("w", encoding="utf-8") as f:
        json.dump(doc_id_to_url, f)

if __name__ == "__main__":
    start = time.perf_counter()

    doc_id = 0
    for json_file in root.rglob("*.json"):
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        url = data.get("url")
        html = data.get("content", "")

        if not url or not html:
            continue

        current_id = doc_id
        doc_id_to_url.append(url)
        doc_id += 1

        index_document(current_id, html, inverted_index)
    
    end = time.perf_counter()
    elapsed = end - start
    save_docs_to_disk(doc_id_to_url)
    save_index_to_disk(inverted_index)

    print("Unique tokens:", len(inverted_index))
    print("Indexed Documents #: ", len(doc_id_to_url))
    print(f"Time elapsed: {elapsed:.4f} seconds")

