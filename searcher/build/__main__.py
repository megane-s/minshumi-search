import os

from dotenv import load_dotenv

from searcher.build.download import download_shared_index

load_dotenv()

print(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
)
download_shared_index()
