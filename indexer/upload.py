import os
import zipfile
from datetime import datetime
from pathlib import Path

from google.cloud import storage

from indexer.settings import INDEXER_TMP_DIR


def upload():
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print(
        "start archive for upload fast text model",
        INDEXER_TMP_DIR, "->", filename,
    )

    # zip に圧縮
    os.makedirs("upload", exist_ok=True)
    zipfile_path = os.path.join("upload", filename+".zip")
    with zipfile.ZipFile(zipfile_path, "w", compression=zipfile.ZIP_DEFLATED) as f:
        for root, _, files in os.walk(INDEXER_TMP_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = Path(file_path).relative_to(INDEXER_TMP_DIR)
                f.write(file_path, relative_path)

    print("end archive for upload fast text model", INDEXER_TMP_DIR)

    # GCSにアップロード
    print("start upload fast text model", zipfile_path)
    client = storage.Client()
    bucket = client.bucket(os.environ["GCS_BUCKET"])
    file = bucket.blob(filename)
    file.upload_from_filename(zipfile_path)
    file = bucket.blob("latest")
    file.upload_from_filename(zipfile_path)
    print("end upload fast text model", filename)
