
from uuid import uuid4

from art.recommend import (GetRecommendArtResultItem, get_recommend_art_by_tag,
                           load_search_index)
from user.db.get import UsersIter
from user.notification.add import add_notifications
from user.type import Notification


def flatten(li: list):
    print(li)
    return sum(li, [])


def recommend_result_to_notification(user_id: str, recommend_result: GetRecommendArtResultItem) -> Notification:
    recommend_result.art
    return Notification(
        notification_id=str(uuid4()),
        type="recommend",
        content=f"{recommend_result.art.art_id}",
        user_id=user_id,
    )


load_search_index()


for user in UsersIter():
    print(user.name, user.interest_tags)
    recommend_results: list[GetRecommendArtResultItem] = flatten(
        list(
            filter(
                lambda result: result is not None,
                [
                    get_recommend_art_by_tag(tag)
                    for tag in user.interest_tags
                ],
            ),
        )
    )
    print([res.art for res in recommend_results])
    add_notifications(
        [
            recommend_result_to_notification(
                user.id, result
            ) for result in recommend_results
        ]
    )
