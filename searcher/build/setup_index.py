from indexer.update_local_index import update_local_index
from searcher.settings import SEARCHER_TMP_DIR


def setup_index():
    update_local_index(SEARCHER_TMP_DIR)
