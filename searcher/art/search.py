import os
from typing import cast

import gensim
import numpy as np
import voyager

from art.get import get_arts_by_search_ids
from searcher.art.type import SearchResultArt
from searcher.settings import SEARCHER_TMP_DIR
from text_vectorize.to_vector import text_to_vector


def init_for_search():
    fast_text_model_path = os.path.join(
        SEARCHER_TMP_DIR,
        "search/art",
        "fast_text.model",
    )
    voyager_index_path = os.path.join(
        SEARCHER_TMP_DIR,
        "search/art",
        "index.voy",
    )

    # validation
    if not os.path.exists(fast_text_model_path):
        raise NotImplementedError(
            f"invalid fast_text_model . it have to exists {fast_text_model_path} . please try to 'python -m searcher.build'",
        )
    if not os.path.exists(voyager_index_path):
        raise NotImplementedError(
            f"invalid voyager_index . it have to exists {voyager_index_path} . please try to 'python -m searcher.build'",
        )

    global model
    model = gensim.models.FastText.load(fast_text_model_path)

    global search_index
    search_index = voyager.Index.load(voyager_index_path)


def search_art(q: str):
    # q を分割
    q_words = q.replace("　", " ").split(" ")
    # q_wordsをそれぞれベクトルに変換
    global model
    vectors = map(lambda q_word: text_to_vector(model, q_word), q_words)
    # ベクトルをそれぞれ検索
    global search_index
    query_results = map(lambda q_vec: search_index.query(q_vec, k=5), vectors)
    # 整形
    output = []
    for query_result in query_results:
        neighbors, distances = cast(
            tuple[np.ndarray, np.ndarray],
            query_result,
        )
        neighbors = get_arts_by_search_ids(neighbors.tolist())
        # TODO distanceが低いものは無視
        output += [
            SearchResultArt.from_art(
                neighbor,
                distance=float(distances[i]),
            ) for i, neighbor in enumerate(neighbors)
        ]
    return output
