from typing import List
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///data/bible/bible.db", echo=True)


class Base(DeclarativeBase):
    pass


class Testament(Base):
    __tablename__ = "testament"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    books: Mapped[List["Book"]] = relationship(back_populates="testament")

    def __repr__(self):
        return f"<Testament(id={self.id}, name={self.name})>"


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    chapter_count: Mapped[int] = mapped_column()

    testament_id: Mapped[int] = mapped_column(ForeignKey("testament.id"))
    testament: Mapped["Testament"] = relationship(back_populates="books")

    chapters: Mapped[List["Chapter"]] = relationship(back_populates="book")
    verses: Mapped[List["Verse"]] = relationship(back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.name}, chapters={self.chapters})>"


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column(String())

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Book"] = relationship(back_populates="chapters")

    verses: Mapped[List["Verse"]] = relationship(back_populates="chapter")
    cross_references: Mapped[List["CrossReference"]] = relationship(
        back_populates="chapter"
    )
    footnotes = relationship("Footnote", back_populates="chapter")

    def __repr__(self):
        return f"<Chapter(id={self.id}, number={self.number})>"


class Verse(Base):
    __tablename__ = "verse"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column(String())

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    chapter: Mapped["Chapter"] = relationship(back_populates="verses")

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Book"] = relationship(back_populates="verses")

    def __repr__(self):
        return f"<Verse(id={self.id}, verse_num={self.verse_num}, verse_text={self.verse_text})>"


class CrossReference(Base):
    __tablename__ = "cross_reference"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(255))

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    chapter: Mapped["Chapter"] = relationship(back_populates="cross_references")

    def __repr__(self):
        return f"<Verse(id={self.id}, verse_num={self.reference})>"


class Footnote(Base):
    __tablename__ = "footnote"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))

    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    chapter: Mapped["Chapter"] = relationship(back_populates="footnotes")

    def __repr__(self):
        return f"<Footnote(id={self.id}, text={self.text})>"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
