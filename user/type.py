
from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str
    interest_tags: list[str]


@dataclass
class Notification:
    __tablename__ = "Notification"
    notification_id: str
    user_id: str
    content: str
    type: str
