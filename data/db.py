import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db():
    conn = sqlite3.connect("data/bible.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = get_db()
    with open("data/bible/schema.sql") as f:
        conn.executescript(f.read())
    conn.close()


def main():
    init_db()


if __name__ == "__main__":
    main()
