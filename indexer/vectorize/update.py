import os
import pathlib

import gensim

from indexer.settings import INDEXER_TMP_DIR
from indexer.vectorize.art import ArtTitleIterable
from settings import VECTORIZE_MODEL_DIMENSIONS
from util.log import WithLog


# MODEL_PATH = os.path.join(INDEXER_TMP_DIR, "./search/art/fast_text.model")
def get_model_path(base_path: str = INDEXER_TMP_DIR):
    return os.path.join(base_path, "./search/art/fast_text.model")


sentences = ArtTitleIterable()


def update_fast_text_model(base_path: str = INDEXER_TMP_DIR):

    model = _setup_fast_text_model()
    _train_with_art_data(model)
    _save(model, base_path)
    return model


def _setup_fast_text_model():
    with WithLog("init fast text model")as logger:
        model = gensim.models.FastText(
            sentences=sentences,
            vector_size=VECTORIZE_MODEL_DIMENSIONS,
            window=5,
            min_count=1,
            workers=4,
        )
        return model


def _train_with_art_data(model: gensim.models.FastText):
    with WithLog("train fast text model") as logger:
        model.train(
            sentences,
            total_examples=2,
            epochs=1,
        )


def _save(model: gensim.models.FastText, path: str = INDEXER_TMP_DIR):
    parent = pathlib.Path(get_model_path(path)).parent
    with WithLog("save fast text model") as logger:
        os.makedirs(parent, exist_ok=True)
        model.save(get_model_path(path))
