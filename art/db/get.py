
import pickle
from os import getenv
from typing import Any, Callable, Generator

from sqlalchemy.orm import Query, Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from art.db.model import DbArt, DbArtTag
from art.type import Art
from db.engine import get_engine
from util.log import WithLog


class ArtsIter:
    def __init__(
        self,
        query: Callable[[Query], Query] = lambda q: q,
        arts_per_unit: int = 5000,
        limit: int = int(getenv("ART_LIST_LIMIT", "10_000")),
    ) -> None:
        self.arts_per_unit = arts_per_unit
        self.limit = limit
        self.query = query

    def __iter__(self) -> Generator[Art, Any, None]:
        def get_arts_iter(session: Session):
            with WithLog(f"load {self.limit} art ({self.arts_per_unit} per page)") as logger:
                i = 0
                rest = self.limit
                while True:
                    if rest <= 0:
                        break
                    q = session.query(DbArt)
                    q = self.query(q)
                    arts_unit = q \
                        .order_by(DbArt.updateAt.desc()) \
                        .offset(i * self.arts_per_unit) \
                        .limit(min(self.arts_per_unit, rest))\
                        .all()
                    for art in arts_unit:
                        yield art.to_art()
                    if len(arts_unit) != self.arts_per_unit:
                        break
                    rest -= len(arts_unit)
                    i += 1
        engine = get_engine()
        return run_transaction(
            sessionmaker(bind=engine),
            lambda s: get_arts_iter(s),
        )


def get_art_by_recommend_id(recommend_id: int):
    arts = get_arts_by_recommend_ids([recommend_id])
    if len(arts) == 0 or arts[0] is None:
        return None
    return arts[0]


def get_arts_by_recommend_ids(recommend_ids: list[int]) -> list[Art]:
    with open("./tmp/recommend/art/recommend_id_map", "rb") as f:
        recommend_ids_map: dict[int, str] = pickle.load(f)
        art_ids = map(lambda r_id: recommend_ids_map[r_id], recommend_ids)

    def get_arts(session: Session):
        arts = map(
            lambda art_id:
            session
            .query(DbArt)
            .where(DbArt.artId == art_id)
            .first(),
            art_ids
        )
        return [
            art.to_art() if art is not None else None
            for art in arts
        ]
    return run_transaction(
        sessionmaker(bind=get_engine()),
        get_arts,
    )
