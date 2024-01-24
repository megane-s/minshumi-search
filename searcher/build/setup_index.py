from art.recommend.recommend import update_recommend_index
from art.search.search import update_search_index as update_search_art_index
from user.search.search import update_search_index as update_search_user_index
from searcher.settings import SEARCHER_TMP_DIR
from util.log import WithLog


def setup_index():
    with WithLog("ビルド"):
        update_recommend_index()
        update_search_art_index()
        update_search_user_index()
