
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from art.recommend import get_recommend_art_by_art_id, load_search_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    load_search_index()
    yield
    print("end")


# recommend = APIRouter(prefix="/recommend")
recommend = APIRouter(prefix="/recommend",  lifespan=lifespan)


@recommend.get("/art")
async def recommend_art_route(art_id: str):
    recommend_arts = get_recommend_art_by_art_id(art_id)
    return recommend_arts
