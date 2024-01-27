
from typing import List

from fastapi import APIRouter, BackgroundTasks

from art.search.search import get_search_index as get_art_search_index
from art.search.search import init_for_search_art, search_art
from art.search.search import update_search_index as update_search_art_index
from user.search.search import get_search_index as get_user_search_index
from user.search.search import init_for_search_user, search_user
from user.search.search import update_search_index as update_search_user_index

search = APIRouter(prefix="/search")

init_for_search_art()
init_for_search_user()


@search.get("/art", response_model=List[str])
async def search_art_route(q: str):
    res = search_art(q)
    return res


@search.get("/art/index")
async def get_search_art_index_route():
    return get_art_search_index()


@search.post("/art/index")
async def update_search_art_index_route(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_search_art_index)
    return {
        "msg": "OK . update started (not finished) .",
    }


@search.get("/user", response_model=List[str])
async def search_user_route(q: str):
    return search_user(q)


@search.get("/user/index")
async def search_user_index_route():
    return get_user_search_index()


@search.post("/user/index")
async def update_search_user_index_route(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_search_user_index)
    return {
        "msg": "OK . update started (not finished) .",
    }
