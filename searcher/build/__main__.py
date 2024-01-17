import os

from dotenv import load_dotenv

from searcher.build.setup_index import setup_index

load_dotenv()

setup_index()
