
import pickle


class UpdateArtSearchIdBatch:
    def __init__(self) -> None:
        self._updates: dict[int, str] = {}

    def update(self, art_id: str, new_recommend_id: int):
        self._updates[new_recommend_id] = art_id

    def flush(self):
        with open("./tmp/recommend/art/recommend_id_map", "wb") as f:
            pickle.dump(self._updates, f)

    def _update_art_ids(self):
        return [art_id for art_id in self._updates]
