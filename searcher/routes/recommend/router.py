
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from art.recommend import get_recommend_art_by_art_id, init_for_recommend


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    init_for_recommend()
    yield
    print("end")


# recommend = APIRouter(prefix="/recommend")
recommend = APIRouter(prefix="/recommend",  lifespan=lifespan)


@recommend.get("/art")
async def recommend_art_route(art_id: str):
    recommend_arts = get_recommend_art_by_art_id(art_id)
    return recommend_arts
