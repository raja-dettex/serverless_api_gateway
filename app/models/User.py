from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __int__(self, name: str, email: str):
        self.name = name
        self.email = email
