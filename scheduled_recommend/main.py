
from uuid import uuid4

from art.recommend import (GetRecommendArtResultItem, get_recommend_art_by_tag,
                           init_for_recommend)
from user.db.get import UsersIter
from user.notification.add import add_notifications
from user.notification.get import has_recommend_notifications
from user.type import Notification
from util.log import WithLog


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


init_for_recommend()


for user in UsersIter():
    print("user", user.name, "interest tags", user.interest_tags)
    with WithLog(f"scheduled recommend : user={user.name}(userId={user.id})") as logger:
        logger.print(f"interest tags=({' , '.join(user.interest_tags)})")
        with WithLog("get recommends") as logger:
            recommend_results: dict[str, GetRecommendArtResultItem] = {}
            for tag in user.interest_tags:
                recommend_result = get_recommend_art_by_tag(tag)
                if recommend_result is None:
                    continue
                for item in recommend_result:
                    if has_recommend_notifications(user.id, item.art.art_id):
                        continue
                    recommend_results[item.art.art_id] = item
            logger.print("recommend_results", "user", user.id, "results", [
                f"{item.art.title}(artId={item.art.art_id},distance={item.distance})"
                for item in recommend_results.values()
            ])
        with WithLog("send notifications"):
            add_notifications(
                [
                    recommend_result_to_notification(
                        user.id, result_item
                    ) for result_item in recommend_results.values()
                ]
            )
