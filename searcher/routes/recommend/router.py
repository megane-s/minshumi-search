
from fastapi import APIRouter

from art.recommend.recommend import (get_recommend_art_by_art_id,
                                     init_for_recommend)

init_for_recommend()

recommend = APIRouter(prefix="/recommend")


@recommend.get("/art")
async def recommend_art_route(art_id: str, limit: int = 50):
    recommend_arts = get_recommend_art_by_art_id(art_id, limit=limit)
    return recommend_arts
