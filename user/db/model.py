
import enum

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from art.db.model import DbArt
from db.base import Base
from user.type import ArtAppeal, Notification, User

# DBの定義は以下を参照
# https://github.com/megane-s/minshumi-frontend/blob/main/prisma/schema.prisma


class DbUser(Base):
    __tablename__ = "User"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    interestTags = relationship("DbInterestTag", backref="parent", lazy=False)
    artAppeals = relationship("DbArtAppeal", backref="parent", lazy=False)
    watchingArts = relationship("DbWatchingArt", backref="parent", lazy=False)

    def to_user(self):
        return User(
            id=self.id,  # type: ignore
            name=self.name,  # type: ignore
            interest_tags=[row.tag for row in self.interestTags],
            art_appeals=[row.to_art_appeal() for row in self.artAppeals],
            watching_arts=[art for art in self.watchingArts]
        )


class DbInterestTag(Base):
    __tablename__ = "InterestTag"
    userId = Column(String, ForeignKey(DbUser.id), primary_key=True)
    tag = Column(String, primary_key=True)


class DbArtAppeal(Base):
    __tablename__ = "ArtAppeal"
    userId = Column(String, ForeignKey(DbUser.id), primary_key=True)
    artId = Column(String, ForeignKey(DbArt.artId), primary_key=True)
    likePoint = Column(String, nullable=False)

    def to_art_appeal(self):
        return ArtAppeal(
            art_id=self.artId,  # type: ignore
            user_id=self.userId,  # type: ignore
            like_point=self.likePoint,  # type: ignore
        )


class DbWatchingArt(Base):
    __tablename__ = "WatchingArt"
    userId = Column(String, ForeignKey(DbUser.id), primary_key=True)
    artId = Column(String, ForeignKey(DbArt.artId), primary_key=True)


class DbNotification(Base):
    __tablename__ = "Notification"
    notificationId = Column(String, primary_key=True, nullable=False)
    userId = Column(String, nullable=False)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)

    def to_notification(self):
        return Notification(
            notificationId=self.notificationId,  # type: ignore
            userId=self.userId,  # type: ignore
            content=self.content,  # type: ignore
            type=self.type,  # type: ignore
        )

    @staticmethod
    def from_notification(notification: Notification):
        return DbNotification(
            notificationId=notification.notification_id,
            type=notification.type,
            content=notification.content,
            userId=notification.user_id,
        )
