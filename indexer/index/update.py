import os

import gensim
import voyager

from art.db.update import UpdateArtSearchIdBatch
from indexer.settings import INDEXER_TMP_DIR
from indexer.vectorize.art import ArtIterable
from settings import VECTORIZE_MODEL_DIMENSIONS
from text_vectorize.to_vector import text_to_vector
from util.log import WithLog

# SEARCH_INDEX_PATH = os.path.join(INDEXER_TMP_DIR, "search/art", "index.voy")


def get_search_index_path(base_path: str = INDEXER_TMP_DIR):
    return os.path.join(base_path, "search/art", "index.voy")


def update_search_index(model: gensim.models.Word2Vec, base_path: str = INDEXER_TMP_DIR):
    index = _setup()
    _train_with_art_data(index, model)
    index.save(get_search_index_path(base_path))


def _setup() -> voyager.Index:
    with WithLog("init search index") as logger:
        model = voyager.Index(
            voyager.Space.Euclidean,
            num_dimensions=VECTORIZE_MODEL_DIMENSIONS,
        )
        return model


def _train_with_art_data(index: voyager.Index, model: gensim.models.Word2Vec):
    with WithLog("train search index") as logger:
        arts = ArtIterable()
        batch = UpdateArtSearchIdBatch()
        for art in arts:
            search_id = index.add_item(
                text_to_vector(model, art.title),
            )
            batch.update(art.art_id, search_id)
        batch.flush()
