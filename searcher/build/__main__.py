
from dotenv import load_dotenv

from searcher.build.setup_index import setup_index
from util.log import WithLog

with WithLog("searcher.build"):
    load_dotenv()
    setup_index()
