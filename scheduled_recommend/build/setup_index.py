from art.recommend.recommend import update_recommend_index
from util.log import WithLog


def setup_index():
    with WithLog("update recommend index"):
        update_recommend_index()
