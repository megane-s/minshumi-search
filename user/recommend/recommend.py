
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

    # TODO 作品アピールや今見ている作品による探索

    # 興味のあるタグによる探索
    for tag in user.interest_tags:
        if len(recommend_results) >= limit:
            break
        recommend_result = get_recommend_art_by_tag(tag)
        if recommend_result is None:
            continue
        for item in recommend_result:
            if len(recommend_results) >= limit:
                break
            if has_recommend_notifications(user.id, item.art.art_id):
                continue
            recommend_results[item.art.art_id] = item

    return recommend_results
