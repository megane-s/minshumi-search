
from dotenv import load_dotenv

from indexer.index.update import update_search_index
from indexer.upload import upload
from indexer.vectorize.update import update_fast_text_model
from indexer.vectorize.upload import upload_fast_text_model

load_dotenv()


def update_shared_index():
    model = update_fast_text_model()

    update_search_index(model)

    upload()


update_shared_index()
