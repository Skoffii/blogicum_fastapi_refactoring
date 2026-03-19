from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///../db/sqlite3"

engine = create_engine(DATABASE_URL)

sessionMake = sessionmaker(bind=engine)

Base = declarative_base()


@contextmanager
def get_session():
    session = sessionMake()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close
