from typing import Any, Generator

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from db.engine import get_engine
from user.db.model import DbUser
from user.type import User


class UsersIter:
    def __iter__(self) -> Generator[User, Any, None]:
        def get_arts_iter(session: Session):
            users = session.query(DbUser).all()
            for user in users:
                yield user.to_user()
        return run_transaction(
            sessionmaker(bind=get_engine()),
            lambda s: get_arts_iter(s),
        )


def get_user(user_id: str) -> User | None:
    def get(session: Session):
        user = session.query(DbUser) \
            .where(DbUser.id == user_id) \
            .limit(1).first()
        return user.to_user() if user is not None else None
    return run_transaction(
        sessionmaker(bind=get_engine()),
        get,
    )
