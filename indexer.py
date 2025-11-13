
#TODO: Number of unique tokens
#TODO: Total size (in KB) of your index on disk
#TODO: OPTIONAL save the time it takes

from readability import Document
from bs4 import BeautifulSoup
import json
from pathlib import Path
from nltk.tokenize import RegexpTokenizer

#Number of indexed documents
tokenizer = RegexpTokenizer(r"\w+")

def tokenize_text(text: str):
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return tokens

def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text

def file_loader():
    n = 0
    root = Path("DEV")

    for json_file in root.rglob("*.json"):
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            n += 1
        # print("Extracted:", extract_main_text(data["content"]))

    print("Indexed Documents #: ", n)

file_loader()
