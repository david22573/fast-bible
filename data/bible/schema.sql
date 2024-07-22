CREATE TABLE
    IF NOT EXISTS BibleVersion (id INTEGER PRIMARY KEY, bible_version TEXT);

CREATE TABLE
    IF NOT EXISTS Testament (
        id INTEGER PRIMARY KEY,
        testament_name TEXT,
        bible_version_id INTEGER,
        FOREIGN KEY (bible_version_id) REFERENCES BibleVersion (id)
    );

CREATE TABLE
    IF NOT EXISTS Book (
        id INTEGER PRIMARY KEY,
        book_name TEXT,
        testament_id INTEGER,
        FOREIGN KEY (testament_id) REFERENCES Testament (id)
    );

CREATE TABLE
    IF NOT EXISTS Chapter (
        id INTEGER PRIMARY KEY,
        chapter_number INTEGER,
        book_id INTEGER,
        FOREIGN KEY (book_id) REFERENCES Book (id)
    );

CREATE TABLE
    IF NOT EXISTS Verse (
        id INTEGER PRIMARY KEY,
        verse_text TEXT,
        verse_number INTEGER,
        verse_type TEXT,
        chapter_id INTEGER,
        FOREIGN KEY (chapter_id) REFERENCES Chapter (id)
    );

CREATE TABLE
    IF NOT EXISTS Footnote (
        id INTEGER PRIMARY KEY,
        footnote_text TEXT,
        verse_id INTEGER,
        FOREIGN KEY (verse_id) REFERENCES Verse (id)
    );

CREATE TABLE
    IF NOT EXISTS CrossReference (
        id INTEGER PRIMARY KEY,
        from_verse_id INTEGER,
        to_verse_id INTEGER,
        FOREIGN KEY (from_verse_id) REFERENCES Verse (id),
        FOREIGN KEY (to_verse_id) REFERENCES Verse (id)
    );