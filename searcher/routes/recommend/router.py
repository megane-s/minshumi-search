
from fastapi import APIRouter

from art.recommend.recommend import (get_recommend_art_by_art_id,
                                     get_recommend_art_by_tag,
                                     init_for_recommend)
from user.recommend.recommend import get_recommendations

init_for_recommend()

recommend = APIRouter(
    prefix="/recommend",
    deprecated=True,
)


@recommend.get("/art")
async def recommend_art_route(art_id: str, limit: int = 50):
    recommend_arts = get_recommend_art_by_art_id(art_id, limit=limit)
    return recommend_arts


@recommend.get("/tag")
async def recommend_tag_route(art_id: str):
    recommend_arts = get_recommend_art_by_tag(art_id)
    return recommend_arts


@recommend.get("/user")
async def recommend_user_route(user_id: str):
    recommend_arts = get_recommendations(user_id)
    return recommend_arts
