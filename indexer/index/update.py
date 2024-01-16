import os

import gensim
import voyager

from indexer.settings import INDEXER_TMP_DIR
from indexer.vectorize.art import ArtTitleIterable
from settings import VECTORIZE_MODEL_DIMENSIONS
from text_vectorize.to_vector import text_to_vector

SEARCH_INDEX_PATH = os.path.join(INDEXER_TMP_DIR, "search/art", "index.voy")


def update_search_index(model: gensim.models.Word2Vec):
    index = _setup()
    _train_with_art_data(index, model)
    index.save(SEARCH_INDEX_PATH)


def _setup() -> voyager.Index:
    if os.path.exists(SEARCH_INDEX_PATH):
        print("start load search index", SEARCH_INDEX_PATH)
        model = voyager.Index.load(SEARCH_INDEX_PATH)
        print("end load search index", SEARCH_INDEX_PATH)
    else:
        print("start init search index", SEARCH_INDEX_PATH)
        model = voyager.Index(
            voyager.Space.Euclidean,
            num_dimensions=VECTORIZE_MODEL_DIMENSIONS,
        )
        print("end init search index", SEARCH_INDEX_PATH)
    return model


def _train_with_art_data(index: voyager.Index, model: gensim.models.Word2Vec):
    print("start train search index")
    art_titles = ArtTitleIterable()
    for title in art_titles:
        index.add_item(text_to_vector(model, title))
    print("end train search index")
