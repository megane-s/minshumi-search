
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from db.engine import get_engine
from user.db.model import DbNotification


def has_recommend_notifications(user_id: str, art_id: str):
    def add(session: Session):
        notifications_count = session.query(DbNotification) \
            .where(DbNotification.userId == user_id) \
            .where(DbNotification.type == "recommend") \
            .where(DbNotification.content == art_id) \
            .limit(1) \
            .count()
        return notifications_count >= 1
    return run_transaction(
        sessionmaker(bind=get_engine()),
        add,
    )
