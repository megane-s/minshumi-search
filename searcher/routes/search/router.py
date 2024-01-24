
from fastapi import APIRouter

from art.search.search import init_for_search_art, search_art
from user.search.search import init_for_search_user, search_user

search = APIRouter(prefix="/search")

init_for_search_art()
init_for_search_user()


@search.get("/art")
async def search_art_route(q: str):
    res = search_art(q)
    return res


@search.get("/user")
async def search_user_route(q: str):
    return search_user(q)
