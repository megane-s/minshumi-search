
from art.recommend.recommend import (GetRecommendArtResultItem,
                                     get_recommend_art_by_art_id,
                                     get_recommend_art_by_tag)
from user.db.get import get_user
from user.notification.get import has_recommend_notifications
from user.type import User


def get_recommendations(user: str | User, limit: int = 5):
    if isinstance(user, str):
        searched_user = get_user(user)
        if searched_user is None:
            return None
        else:
            user = searched_user

    recommend_results: dict[str, GetRecommendArtResultItem] = {}

    for item in recommend_iter(user):
        if len(recommend_results) >= limit:
            break
        if has_recommend_notifications(user.id, item.art.art_id):
            continue
        recommend_results[item.art.art_id] = item

    return recommend_results


def recommend_iter(user: User):
    for appeal in user.art_appeals:
        recommend_result = get_recommend_art_by_art_id(appeal.art_id)
        if recommend_result is None:
            continue
        for art in recommend_result:
            yield art

    for tag in user.interest_tags:
        recommend_result = get_recommend_art_by_tag(tag)
        if recommend_result is None:
            continue
        for art in recommend_result:
            yield art

    for art in user.watching_arts:
        recommend_result = get_recommend_art_by_art_id(art.art_id)
        if recommend_result is None:
            continue
        for art in recommend_result:
            yield art
