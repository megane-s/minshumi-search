
import os

from fastapi import FastAPI

from searcher.routes.recommend.router import recommend

# from searcher.routes.search.router import search

app = FastAPI()
# app.include_router(search)
app.include_router(recommend)


@app.get("/")
async def test():
    return {"msg": "ok", "tmp_exists": os.path.exists("./tmp/searcher")}
