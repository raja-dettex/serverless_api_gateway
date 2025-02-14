from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..models.User import Base
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URI")

engine = create_engine(url=DATABASE_URL)
sessionLocal = sessionmaker(bind=engine)


def init_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    session = sessionLocal()
    if session is not None:
        yield session
    session.close()
