
import os
import pickle

from art.db.get import ArtsIter
from art.db.model import DbArt
from art.recommend.index.split_word import split_text
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
            print(words)
    with WithLog("save search index"):
        os.makedirs("./tmp/search/art/", exist_ok=True)
        with open("./tmp/search/art/index.pickle", "wb") as f:
            pickle.dump(index, f)


def _ngram_split_title(title: str) -> list[str]:
    return [
        title
    ] + split_text(title)


def _split_art_words(art: Art):
    result = []
    result += split_text(art.title)
    result += art.tags
    result += split_text(art.description)
    return result

# search


def init_for_search_art():
    load_search_index()


def load_search_index():
    global _search_index
    with open("./tmp/search/art/index.pickle", "rb") as f:
        _search_index = pickle.load(f)


def ge_search_index():
    global _search_index
    return _search_index


def search_art(q: str):
    q_words = split_text(q)
    print(q, ">>", q_words)
    index = ge_search_index()
    res = []
    for q_w in q_words:
        if q_w not in index:
            continue
        res += index[q_w]
    return [*set(res)]
