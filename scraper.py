import requests
from bs4 import BeautifulSoup

import time
import json

import re

from app.db import Testament, Book, Chapter, Verse
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
    new_passage = "".join(new_passage)
    return new_passage


def add_verses(verses, book_id, chapter_id):
    verses = [
        Verse(
            number=i,
            text=verses[i - 1],
            chapter_id=chapter_id,
            book_id=book_id,
        )
        for i in range(1, len(verses) + 1)
    ]
    bible_db.session.add_all(verses)
    bible_db.session.commit()


def scrape_books():
    bible_structure = json.load(open("data/bible/books.json"))

    for testament in bible_structure["bible"]["testaments"]:
        testament_db = Testament(name=testament["name"])
        bible_db.session.add(testament_db)
        bible_db.session.commit()
        for book in testament["books"]:
            book_db = Book(
                name=book["name"],
                testament_id=testament_db.id,
                chapter_count=book["chapters"],
            )
            bible_db.session.add(book_db)
            bible_db.session.commit()
            for chapter in range(1, book["chapters"] + 1):
                passage = scrape_content(book["name"], chapter)
                passage = clean_passage(passage)
                verses = [v for v in passage.split("\n") if v[0].isdigit()]
                chapter_db = Chapter(number=chapter, text=passage, book_id=book_db.id)
                bible_db.session.add(chapter_db)
                bible_db.session.commit()
                add_verses(verses, book_db.id, chapter_db.id)
                time.sleep(5)  # Additional delay between chapters

            time.sleep(10)  # Additional delay between books


def main():
    scrape_books()


if __name__ == "__main__":
    main()
