import sqlite3
import requests
import time
from bs4 import BeautifulSoup
import json


# Database setup
def setup_database():
    conn = sqlite3.connect("bible.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS verses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book TEXT,
                  chapter INTEGER,
                  verse INTEGER,
                  text TEXT)"""
    )
    conn.commit()
    return conn


# Scraping and database insertion
session = requests.Session()
session.headers.update({"User-Agent": "FastBible/1.0 (davidmiguel22573@gmail.com)"})


def get_page(url):
    response = session.get(url)
    time.sleep(2)  # Wait 2 seconds between requests
    return BeautifulSoup(response.content, "html.parser")


def scrape_chapter(book, chapter, conn):
    url = f"https://www.biblegateway.com/passage/?search={book}+{chapter}&version=ESV"
    try:
        soup = get_page(url)
        verses = soup.select("div.passage-text p.verse")
        c = conn.cursor()
        for verse in verses:
            verse_num = verse.find("span", class_="verse-num").text.strip()
            verse_text = "".join(verse.find_all(text=True, recursive=False)).strip()
            c.execute(
                "INSERT INTO verses (book, chapter, verse, text) VALUES (?, ?, ?, ?)",
                (book, chapter, int(verse_num), verse_text),
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error scraping {book} {chapter}: {str(e)}")
        return False


def main():
    conn = setup_database()
    bible_structure = json.load(open("data/books.json"))

    for testament in bible_structure["bible"]["testaments"]:
        for book in testament["books"]:
            for chapter in range(1, book["chapters"] + 1):
                success = scrape_chapter(book["name"], chapter, conn)
                if success:
                    print(f"Scraped {book['name']} chapter {chapter}")
                time.sleep(5)  # Additional delay between chapters

            print(f"Completed scraping {book['name']}")
            time.sleep(10)  # Additional delay between books

    conn.close()


if __name__ == "__main__":
    main()
