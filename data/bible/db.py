from ..db import get_db
from .models import Book, Chapter, Verse


def add_book(book: Book):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO books (name, chapters) VALUES (?, ?)",
            (book.name, book.chapters),
        )
        conn.commit()


def add_chapter(chapter: Chapter):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO chapters (book, number) VALUES (?, ?)",
            (chapter.book, chapter.number),
        )
        conn.commit()


def add_verse(verse: Verse):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO verses (book, chapter, verse, text) VALUES (?, ?, ?, ?)",
            (verse.book, verse.chapter, verse.verse, verse.text),
        )
        conn.commit()
