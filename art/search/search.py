
import os
import pickle
import re

from art.db.get import ArtsIter
from art.db.model import DbArt
from art.recommend.index.split_word import split_by_ngrams, split_text
from art.type import Art
from util.log import WithLog

# build


def update_search_index():
    with WithLog("update search index"):
        index = {}
        for art in ArtsIter():
            art: Art = art
            words = _split_art_words(art)
            for word in words:
                if word in index:
                    index[word].insert(0, art.art_id)
                else:
                    index[word] = [art.art_id]
    with WithLog("save search index"):
        os.makedirs("./tmp/search/art/", exist_ok=True)
        with open("./tmp/search/art/index.pickle", "wb") as f:
            pickle.dump(index, f)


def _split_art_words(art: Art):
    result = []
    result += [art.art_id]
    result += split_text(art.title)
    result += split_by_ngrams(art.title)
    result += art.tags
    result += split_text(art.description)
    result += split_by_ngrams(art.description, min=10, max=len(art.title))
    return [*set(result)]

# search


def init_for_search_art():
    load_search_index()


def load_search_index():
    global _search_index
    with open("./tmp/search/art/index.pickle", "rb") as f:
        _search_index = pickle.load(f)


def get_search_index():
    global _search_index
    return _search_index


def search_art(q: str):
    q_words = re.split(r"\s+", q)
    index = get_search_index()
    res = []
    for q_w in q_words:
        if q_w not in index:
            continue
        res += index[q_w]
    return [*set(res)]
