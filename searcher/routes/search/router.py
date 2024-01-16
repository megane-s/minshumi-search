
from fastapi import APIRouter

from searcher.art.search import init_for_search, search_art

search = APIRouter(prefix="/search")

init_for_search()


@search.get("/art")
async def search_art_route(q: str):
    res = search_art(q)
    return res


@search.get("/user")
async def search_user(q: str):
    raise NotImplementedError("search user")
