from pydantic import BaseModel


class BibleVersion(BaseModel):
    version: str


class Testament(BaseModel):
    name: str


class Book(BaseModel):
    name: str
    chapters: int


class Chapter(BaseModel):
    number: int
    book: str


class Verse(BaseModel):
    verse: int
    text: str
