from art.recommend.recommend import update_recommend_index
from searcher.settings import SEARCHER_TMP_DIR
from util.log import WithLog


def setup_index():
    with WithLog("ビルド"):
        update_recommend_index()
