
import os

import joblib
from nltk import ngrams

from art.recommend.index.split_word import split_by_ngrams, split_text
from user.db.get import UsersIter
from user.type import User
from util.log import WithLog

# build


def update_search_index():
    with WithLog("update search index"):
        index: dict[str, list[str]] = {}
        for user in UsersIter():
            user: User = user
            words = _split_user_words(user)
            for word in words:
                if word in index:
                    if user.id in index[word]:
                        continue
                    index[word].insert(0, user.id)
                else:
                    index[word] = [user.id]
    with WithLog("save search index"):
        os.makedirs("./tmp/search/user/", exist_ok=True)
        with open("./tmp/search/user/index", "wb") as f:
            joblib.dump(index, f)


def _split_user_words(user: User) -> list[str]:
    result: list[str] = []
    result += [user.id]
    result += split_text(user.name)
    result += split_by_ngrams(user.name)
    for i in range(2, len(user.name)):
        if 20 <= i:
            break
        result += list(ngrams(user.name, i))
    return [*set(result)]

# search


def init_for_search_user():
    load_search_index()


def load_search_index():
    global _search_index
    with open("./tmp/search/user/index", "rb") as f:
        _search_index = joblib.load(f)


def get_search_index():
    global _search_index
    return _search_index


def search_user(q: str):
    q_words = split_text(q)
    index = get_search_index()
    res = []
    for q_w in q_words:
        if q_w not in index:
            continue
        print(index[q_w])
        res += index[q_w]
    return [*set(res)]
