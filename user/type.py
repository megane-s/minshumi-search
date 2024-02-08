
from dataclasses import dataclass

from art.type import Art


@dataclass
class ArtAppeal:
    art_id: str
    user_id: str
    like_point: str


@dataclass
class User:
    id: str
    name: str
    interest_tags: list[str]
    art_appeals: list[ArtAppeal]
    watching_art_ids: list[str]


@dataclass
class Notification:
    __tablename__ = "Notification"
    notification_id: str
    user_id: str
    content: str
    type: str
