from sqlalchemy.orm import Session

from . import engine


class BibleDB:
    def __init__(self):
        self.session = Session(bind=engine)
