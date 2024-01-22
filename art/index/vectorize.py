
import os
from functools import cache
from itertools import tee
from pathlib import Path

import gensim
import numpy as np

from art.db.get import AllArts
from art.index.split_word import split_text
from art.type import Art

# TITLE_DIMENSIONS = 20
# DESCRIPTION_DIMENSIONS = 10
# TAGS_DIMENSIONS = 50


# arts_for_title, arts_for_description, arts_for_tags = tee(AllArts(), 3)


# @cache
# def get_title_vectorize_model():
#     def art_titles():
#         for art in arts_for_title:
#             yield split_text(art.title)
#     model = gensim.models.FastText(
#         sentences=art_titles(),
#         vector_size=TITLE_DIMENSIONS,
#     )
#     model.save("./tmp/search/art/vectorize/title.model")
#     return model


# @cache
# def get_description_vectorize_model():
#     def art_descriptions():
#         for art in arts_for_description:
#             yield split_text(art.description)
#     model = gensim.models.FastText(
#         sentences=art_descriptions(),
#         vector_size=DESCRIPTION_DIMENSIONS,
#     )
#     model.save("./tmp/search/art/vectorize/description.model")
#     return model


# @cache
# def get_tags_vectorize_model():
#     def art_tags():
#         for art in arts_for_tags:
#             yield art.tags
#     model = gensim.models.FastText(
#         sentences=art_tags(),
#         vector_size=TAGS_DIMENSIONS,
#     )
#     model.save("./tmp/search/art/vectorize/tags.model")
#     return model

@cache
def get_art_vectorize_model():
    model = gensim.models.Doc2Vec(
        documents=[
            gensim.models.doc2vec.TaggedDocument(
                [
                    *split_text(art.title),
                    *art.tags,
                    *split_text(art.description),
                ],
                [art.art_id],
            ) for art in AllArts()
        ],
        vector_size=300,
        window=5,
        min_count=1,
        workers=4,
        epochs=20,
    )
    os.makedirs(
        Path("./tmp/search/art/vectorize/art.model").parent,
        exist_ok=True,
    )
    model.save("./tmp/search/art/vectorize/art.model")
    return model
