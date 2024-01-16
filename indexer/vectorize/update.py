import os
import pathlib
from typing import cast

import gensim

from indexer.settings import INDEXER_TMP_DIR
from indexer.vectorize.art import ArtTitleIterable
from settings import VECTORIZE_MODEL_DIMENSIONS

MODEL_PATH = os.path.join(INDEXER_TMP_DIR, "./search/art/fast_text.model")

# TODO
sentences = ArtTitleIterable()


def update_fast_text_model():
    model = _setup_fast_text_model()
    _train_with_art_data(model)
    _save(model)
    return model


def _setup_fast_text_model():
    if os.path.exists(MODEL_PATH):
        print("start load fast text model", MODEL_PATH)
        model = cast(
            gensim.models.FastText,
            gensim.models.FastText.load(MODEL_PATH),
        )
        print("finish load save fast text model")
        return model
    else:
        print("init fast text model")
        model = gensim.models.FastText(
            sentences=sentences,
            vector_size=VECTORIZE_MODEL_DIMENSIONS,
            window=5,
            min_count=1,
            workers=4,
        )
        print("finish init fast text model")
        return model


def _train_with_art_data(model: gensim.models.FastText):
    print("start train fast text model")
    model.train(
        sentences,
        total_examples=2,
        epochs=1,
    )
    print("finish train fast text model")


def _save(model: gensim.models.FastText):
    parent = pathlib.Path(MODEL_PATH).parent
    print("start save fast text model", parent)
    os.makedirs(parent, exist_ok=True)
    model.save(MODEL_PATH)
    print("finish save fast text model")
