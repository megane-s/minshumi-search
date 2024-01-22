
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from art.db.model import DbArt
from db.engine import get_engine


class UpdateArtSearchIdBatch:
    def __init__(self) -> None:
        self._updates: dict[str, int] = {}

    def update(self, art_id: str, new_search_id: int):
        self._updates[art_id] = new_search_id

    def flush(self):
        engine = get_engine()

        def update(session: Session):
            q = session.query(DbArt)
            q = q.filter(DbArt.artId.in_(self._update_art_ids()))
            arts = q.all()
            for art in arts:
                print("update search id", art.artId)
                new_search_id = self._updates[art.artId]  # type: ignore
                art.searchId = new_search_id  # type: ignore
        return run_transaction(
            sessionmaker(bind=engine),
            lambda s: update(s),
        )

    def _update_art_ids(self):
        return [art_id for art_id in self._updates]
