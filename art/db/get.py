
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
    engine = get_engine()

    def get_arts(session: Session, recommend_ids: list[int]) -> list[Art | None]:
        def get_art(recommend_id: int):
            art = session.query(DbArt) \
                .filter(DbArt.recommendId == recommend_id) \
                .first()
            if art is None:
                return None
            return art.to_art()
        result = [
            get_art(recommend_id) for recommend_id in recommend_ids
        ]
        return result
    return run_transaction(
        sessionmaker(bind=engine),
        lambda s: get_arts(s, recommend_ids),
    )
