
import json
import os
from dataclasses import dataclass
from itertools import tee
from pathlib import Path
from typing import cast

import gensim
from voyager import Index, Space

from art.db.get import ArtsIter, get_arts_by_recommend_ids
from art.db.update import UpdateArtSearchIdBatch
from art.index.split_word import split_text
from art.index.vectorize import ART_VECTOR_DIMENSIONS, get_art_vectorize_model
from art.type import Art
from settings import DATA_BASE_DIR
from util.log import WithLog


def get_recommend_index_path(base_path: str = DATA_BASE_DIR):
    return os.path.join(base_path, "search/art", "index.voy")


def update_recommend_index():
    arts_for_vectorize, arts_for_index = tee(ArtsIter(), 2)
    with WithLog("load vectorize model"):
        vec_model = get_art_vectorize_model(arts_for_vectorize)
        art_recommend_index = Index(
            Space.Euclidean,
            num_dimensions=ART_VECTOR_DIMENSIONS,
        )

    with WithLog("update recommend index"):
        batch = UpdateArtSearchIdBatch()
        for art in arts_for_index:
            art_recommend_vec = vec_model.dv[art.art_id]
            recommend_id = art_recommend_index.add_item(art_recommend_vec)
            batch.update(art.art_id, recommend_id)
        with WithLog("flush"):
            batch.flush()

    with WithLog("save recommend index"):
        os.makedirs(Path(get_recommend_index_path()).parent, exist_ok=True)
        art_recommend_index.save(get_recommend_index_path())


def load_recommend_index():
    with WithLog("load recommend index"):
        global _index
        _index = Index.load(get_recommend_index_path())


def get_recommend_index():
    global _index
    return _index


def load_vec_model():
    with WithLog("load vec model"):
        global _vec_model
        _vec_model = cast(
            gensim.models.Doc2Vec,
            gensim.models.Doc2Vec.load(
                "./tmp/search/art/vectorize/art.model"
            ),
        )


def get_vec_model():
    global _vec_model
    return _vec_model


def init_for_recommend():
    load_recommend_index()
    load_vec_model()


@dataclass
class GetRecommendArtResultItem:
    art: Art
    distance: float


def get_recommend_art_by_art_id(art_id: str):
    index = get_recommend_index()
    vec_model = get_vec_model()
    if art_id not in vec_model.dv:
        return None
    with WithLog("recommend"):
        neighbors, distances = index.query(
            vec_model.dv[art_id],
            k=min(len(index), 20),
        )
    with WithLog(f"fetch art data"):
        arts = get_arts_by_recommend_ids(neighbors.tolist())
    return [GetRecommendArtResultItem(art, float(distances[i])) for i, art in enumerate(arts)]


def get_recommend_art_by_tag(tag: str):
    # 中身のやることは同じなのでart_id版を呼び出し
    return get_recommend_art_by_art_id(tag)
