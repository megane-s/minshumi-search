
from fastapi import APIRouter

from art.recommend import get_recommend_art_by_art_id, init_for_recommend

init_for_recommend()

recommend = APIRouter(prefix="/recommend")


@recommend.get("/art")
async def recommend_art_route(art_id: str):
    recommend_arts = get_recommend_art_by_art_id(art_id)
    return recommend_arts
