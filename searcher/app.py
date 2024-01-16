
import os

from fastapi import FastAPI

from searcher.routes.search.router import search

app = FastAPI()
app.include_router(search)


@app.get("/")
async def test():
    return {"msg": "ok", "tmp_exists": os.path.exists("./tmp/searcher")}
