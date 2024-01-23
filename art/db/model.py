
import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from art.type import Art
from db.base import Base

# DBの定義は以下を参照
# https://github.com/megane-s/minshumi-frontend/blob/main/prisma/schema.prisma


class DbArt(Base):
    __tablename__ = "Art"

    artId = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    recommendId = Column(Integer, nullable=True)

    tags = relationship("DbArtTag", backref="parent", lazy=False)

    createAt = Column(DateTime)
    updateAt = Column(DateTime)

    def to_art(self):
        return Art(
            art_id=self.artId,  # type: ignore
            title=self.title,  # type: ignore
            recommend_id=self.recommendId,  # type: ignore
            description=self.description,  # type: ignore
            tags=[tag.tag for tag in self.tags],
        )


class DbArtTagType(enum.Enum):
    MEDIA = 1
    GENRE = 2
    OTHER = 3
    CUSTOM = 4


class DbArtTag(Base):
    __tablename__ = "ArtTag"
    artId = Column(String, ForeignKey(DbArt.artId), primary_key=True)
    tag = Column(String, primary_key=True)
