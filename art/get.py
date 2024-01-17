
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from art.db import DbArt, DbArtTag
from art.type import Art
from db.engine import get_engine


def get_all_arts():
    def get_arts(session: Session):
        res = session.query(DbArt).all()
        return [
            Art(
                art_id=art.artId,  # type: ignore
                title=art.title,  # type: ignore
                description=art.description,  # type: ignore
                search_id=art.searchId,  # type: ignore
                tags=art.tags,
            ) for art in res
        ]
    engine = get_engine()
    return run_transaction(
        sessionmaker(bind=engine),
        lambda s: get_arts(s),
    )


def get_art_by_search_id(search_id: int):
    arts = get_arts_by_search_ids([search_id])
    if len(arts) == 0:
        return None
    return arts[0]


def get_arts_by_search_ids(search_ids: list[int]) -> list[Art]:
    engine = get_engine()

    def get_arts(session: Session, search_ids: list[int]) -> list[Art]:
        q = session.query(DbArt)
        q = q.outerjoin(DbArtTag, DbArt.artId == DbArtTag.artId)
        q = q.filter(DbArt.searchId.in_(search_ids))
        arts = q.all()
        return [
            Art(
                art_id=art.artId,  # type: ignore
                title=art.title,  # type: ignore
                search_id=art.searchId,  # type: ignore
                description=art.description,  # type: ignore
                tags=art.tags,
            ) for art in arts
        ]
    return run_transaction(
        sessionmaker(bind=engine),
        lambda s: get_arts(s, search_ids),
    )