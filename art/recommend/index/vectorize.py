
import os
from functools import cache
from itertools import tee
from pathlib import Path

import gensim
import numpy as np

from art.db.get import ArtsIter
from art.recommend.index.split_word import split_text

ART_VECTOR_DIMENSIONS = 300


@cache
def get_art_vectorize_model(arts: ArtsIter = ArtsIter()):
    model = gensim.models.Doc2Vec(
        documents=[
            gensim.models.doc2vec.TaggedDocument(
                [
                    *split_text(art.title),
                    # *split_text(art.description),
                    *art.tags,
                ],
                [art.art_id, *art.tags],
            ) for art in arts
        ],
        vector_size=ART_VECTOR_DIMENSIONS,
        window=5,
        min_count=1,
        workers=4,
        epochs=20,
    )
    os.makedirs(
        Path("./tmp/recommend/art/vectorize/art.model").parent,
        exist_ok=True,
    )
    model.save("./tmp/recommend/art/vectorize/art.model")
    return model
