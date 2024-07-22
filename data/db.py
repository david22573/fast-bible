import sqlite3


def get_db():
    conn = sqlite3.connect("data/bible.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    with open("data/schema.sql") as f:
        conn.executescript(f.read())
    conn.close()


def main():
    init_db()


if __name__ == "__main__":
    main()
