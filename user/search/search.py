
import os
import pickle

from art.recommend.index.split_word import split_text
from user.db.get import UsersIter
from user.type import User
from util.log import WithLog

# build


def update_search_index():
    with WithLog("update search index"):
        index: dict[str, list[str]] = {}
        for user in UsersIter():
            user: User = user
            words = [*_ngram_split_user_name(user.name), user.id]
            for word in words:
                if word in index:
                    if user.id in index[word]:
                        continue
                    index[word].insert(0, user.id)
                else:
                    index[word] = [user.id]
    with WithLog("save search index"):
        os.makedirs("./tmp/search/user/", exist_ok=True)
        with open("./tmp/search/user/index.pickle", "wb") as f:
            pickle.dump(index, f)


def _ngram_split_user_name(title: str) -> list[str]:
    return [
        title
    ] + split_text(title)

# search


def init_for_search_user():
    load_search_index()


def load_search_index():
    global _search_index
    with open("./tmp/search/user/index.pickle", "rb") as f:
        _search_index = pickle.load(f)


def ge_search_index():
    global _search_index
    return _search_index


def search_user(q: str):
    q_words = split_text(q)
    index = ge_search_index()
    res = []
    for q_w in q_words:
        if q_w not in index:
            continue
        print(index[q_w])
        res += index[q_w]
    return [*set(res)]
