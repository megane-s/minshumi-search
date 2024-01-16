import os
import zipfile
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import storage
from searcher.settings import SEARCHER_TMP_DIR

from settings import DATA_BASE_DIR

load_dotenv()


def download_shared_index():
    print("start download shared index")
    filename = "latest"
    client = storage.Client()
    bucket = client.bucket(os.environ["GCS_BUCKET"])
    file = bucket.blob(filename)
    os.makedirs(DATA_BASE_DIR, exist_ok=True)
    zipfile_path = os.path.join(
        DATA_BASE_DIR, "local-search-index.zip",
    )
    file.download_to_filename(zipfile_path)
    with zipfile.ZipFile(zipfile_path, "r") as f:
        dest = SEARCHER_TMP_DIR
        f.extractall(dest)
    os.remove(zipfile_path)
    print("end download shared index", dest)
