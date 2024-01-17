from dataclasses import dataclass


@dataclass
class Art:
    art_id: str
    title: str
    description: str
    tags: list[str]
    search_id: int
