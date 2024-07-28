import requests
from bs4 import BeautifulSoup

import time
import json

import re

from app.db.bible import BibleDB

bible_db = BibleDB()


def get_page(url):
    session = requests.Session()
    session.headers.update({"User-Agent": "FastBible/1.0 (davidmiguel22573@gmail.com)"})
    response = session.get(url)
    time.sleep(2)  # Wait 2 seconds between requests
    return response.content


def clean_verse(v):
    verse_text = v.get_text()
    verse_text = re.sub(r"(\([A-Z]+\))|(\[[a-z]+\])", "", verse_text)
    if verse_text[-1] == "." or verse_text[:-2] == '."':
        verse_text = verse_text + "\n"
    if verse_text[0].isdigit():
        verse_text = "\n" + verse_text
    return re.sub(r"\xa0", " ", verse_text)


def scrape_content(book, chapter, content=None):
    url = f"https://www.biblegateway.com/passage/?search={book}+{chapter}&version=ESV"
    try:
        if not content:
            content = get_page(url)
        soup = BeautifulSoup(content, "html.parser")
        verses = soup.select("span.text")
        return [clean_verse(v) for v in verses if len(v["class"]) > 1]
    except Exception as e:
        print(f"Error scraping {book} {chapter}: {str(e)}")
        return False


def clean_passage(passage):
    new_passage = []
    for p in passage:
        if p[0].isdigit():
            new_passage.append("\n" + p)
        elif p[-1] == "." or p[:-2] == '."':
            new_passage.append(p + "\n")
        else:
            new_passage.append(p)
    return ("".join(new_passage)).split("\n")


def scrape_books():
    bible_structure = json.load(open("data/bible/books.json"))

    for testament in bible_structure["bible"]["testaments"]:
        for book in testament["books"]:
            for chapter in range(1, book["chapters"] + 1):
                passage = scrape_content(book["name"], chapter)
                print(clean_passage(passage))
                time.sleep(5)  # Additional delay between chapters

            time.sleep(10)  # Additional delay between books


def main():
    with open("test.html", "rb") as content:
        passage = "".join(scrape_content("Mark", 1, content))
        print(len([p for p in passage.split("\n") if p and not p[0].isdigit()]))


if __name__ == "__main__":
    main()
