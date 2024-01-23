from dataclasses import dataclass

from art.type import Art


@dataclass
class SearchResultArt(Art):
    distance: float

    @classmethod
    def from_art(cls, art: Art, distance: float):
        return SearchResultArt(
            art_id=art.art_id,
            title=art.title,
            description=art.description,
            tags=art.tags,
            recommend_id=art.recommend_id,
            distance=distance,
        )
