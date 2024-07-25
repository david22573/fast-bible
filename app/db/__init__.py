from typing import List
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///data/bible.db", echo=True)


class Base(DeclarativeBase):
    pass


class Testaments(Base):
    __tablename__ = "testament"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    books: Mapped[List["Books"]] = relationship(back_populates="testament")

    def __repr__(self):
        return f"<Testament(id={self.id}, name={self.name})>"


class Books(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    chapter_count: Mapped[int] = mapped_column()

    testament_id: Mapped[int] = mapped_column(ForeignKey("testament.id"))
    testament: Mapped["Testaments"] = relationship(back_populates="books")

    chapters: Mapped[List["Verse"]] = relationship(back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.name}, chapters={self.chapters})>"


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Books"] = relationship(back_populates="chapters")

    verses: Mapped[List["Verse"]] = relationship(back_populates="chapter")

    def __repr__(self):
        return f"<Chapter(id={self.id}, number={self.number})>"


class Verse(Base):
    __tablename__ = "verse"

    id: Mapped[int] = mapped_column(primary_key=True)
    verse_num: Mapped[int] = mapped_column()
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    chapter: Mapped["Chapter"] = relationship(back_populates="verses")

    def __repr__(self):
        return f"<Verse(id={self.id}, verse_num={self.verse_num})>"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
