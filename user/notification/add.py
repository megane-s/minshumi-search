from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from db.engine import get_engine
from user.db.model import DbNotification
from user.type import Notification


def add_notifications(notifications: list[Notification]):
    def add(session: Session):
        session.add_all(
            DbNotification.from_notification(notification)
            for notification in notifications
        )
        # TODO 端末に通知を送信
    return run_transaction(
        sessionmaker(bind=get_engine()),
        add,
    )
