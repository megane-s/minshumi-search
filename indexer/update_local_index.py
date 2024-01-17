
from dotenv import load_dotenv

from indexer.index.update import update_search_index
from indexer.settings import INDEXER_TMP_DIR
from indexer.vectorize.update import update_fast_text_model
from util.log import WithLog

load_dotenv()


def update_local_index(path: str = INDEXER_TMP_DIR):
    with WithLog("update local index") as logger:
        logger.print("output to", path)

        model = update_fast_text_model(path)

        update_search_index(model, path)

        # upload()
