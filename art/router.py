
from fastapi import APIRouter

art_search = APIRouter(
    prefix="/art/search",
)


@art_search.get("")
async def search(q: str):
    return {}
