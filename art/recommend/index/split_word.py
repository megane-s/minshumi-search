import MeCab
from nltk import ngrams

from art.recommend.index.normalize_text import normalize_text

wakati = MeCab.Tagger("-Owakati")


def split_text(
    text: str,
    normalize: bool = True,
):
    if normalize:
        text = normalize_text(text)
    return wakati.parse(text).split()


def split_by_ngrams(text: str, min: int = 2, max: int | None = None):
    if max is None:
        max = len(text)
    result: set[str] = set()

    for i in range(min, max):
        grams = ngrams(text, i)
        for g in grams:
            chunk = "".join(g)
            result.add(chunk)

    return result
