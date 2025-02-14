from sqlalchemy.orm import Session
from ..models.User import User
from typing import List


def get_all(db: Session) -> List[User]:
    users = db.query(User).all()
    return list(users)


def add(db: Session, name: str , email: str) -> User:
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, id: int, name: str) -> User:
    user = db.query(User).filter_by(User.id==id).first()
    if user is not None:
        user.name = name
        db.commit()
        db.refresh(user)
    return user


def delete(db: Session, id: int) -> bool:
    user = db.query(User).filter(User.id==id).first()
    if user is not None:
        db.delete(user)
        db.commit()
        return True
    return False
