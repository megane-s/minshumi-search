
from dotenv import load_dotenv

from scheduled_recommend.build.setup_index import setup_index

from util.log import WithLog

with WithLog("scheduled_recommend.build"):
    load_dotenv()
    setup_index()
