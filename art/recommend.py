
import json
import os
from itertools import tee
from pathlib import Path
from typing import cast

import gensim
from voyager import Index, Space

from art.db.get import ArtsIter
from art.db.update import UpdateArtSearchIdBatch
from art.index.split_word import split_text
from art.index.vectorize import ART_VECTOR_DIMENSIONS, get_art_vectorize_model
from settings import DATA_BASE_DIR
from util.log import WithLog


def get_search_index_path(base_path: str = DATA_BASE_DIR):
    return os.path.join(base_path, "search/art", "index.voy")


def update_recommend_index():
    arts_for_vectorize, arts_for_index = tee(ArtsIter(), 2)
    with WithLog("load vectorize model") as logger:
        vec_model = get_art_vectorize_model(arts_for_vectorize)
        art_search_index = Index(
            Space.Euclidean,
            num_dimensions=ART_VECTOR_DIMENSIONS,
        )

    with WithLog("update search index") as logger:
        batch = UpdateArtSearchIdBatch()
        outputs = []
        for art in arts_for_index:
            texts = " ".join([
                *split_text(art.title),
                *split_text(art.description),
                *art.tags,
            ])
            art_vec = vec_model.dv[art.art_id]
            search_id = art_search_index.add_item(art_vec)
            batch.update(art.art_id, search_id)
            # logger.print(art.art_id, texts, ">>>", search_id)
            # outputs.append({
            #     "artId": art.art_id,
            #     "texts": texts,
            #     "searchId": search_id,
            # })
        with WithLog("flush"):
            batch.flush()

    with WithLog("save search index") as logger:
        os.makedirs(Path(get_search_index_path()).parent, exist_ok=True)
        art_search_index.save(get_search_index_path())


def load_search_index():
    with WithLog("load search index"):
        global _index
        _index = Index.load(get_search_index_path())


def get_search_index():
    global _index
    return _index


def get_recommend_art(art_id: str):
    with WithLog("load search index"):
        load_search_index()
    index = get_search_index()
    with WithLog("load vec model"):
        vec_model = cast(
            gensim.models.Doc2Vec,
            gensim.models.Doc2Vec.load(
                "./tmp/search/art/vectorize/art.model"
            ),
        )
        neighbors, distances = index.query(
            vec_model.dv[art_id],
            k=min(len(index), 20),
        )
        print("search result: neighbors:", neighbors)
        print("search result: distances:", distances)
        return []
