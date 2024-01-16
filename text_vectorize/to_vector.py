
import gensim

from word.split import word_split


def text_to_vector(model: gensim.models.Word2Vec, text: str):
    vector = model.wv[text]
    return vector
