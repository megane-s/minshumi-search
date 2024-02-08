
import traceback
from uuid import uuid4

from art.recommend.recommend import (GetRecommendArtResultItem,
                                     get_recommend_art_by_tag,
                                     init_for_recommend)
from user.db.get import UsersIter
from user.notification.add import add_notifications
from user.notification.get import has_recommend_notifications
from user.recommend.recommend import get_recommendations
from user.type import Notification
from util.log import WithLog


def flatten(li: list):
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

errors = []

for user in UsersIter():
    try:
        print("user", user.name, "interest tags", user.interest_tags)
        with WithLog(f"scheduled recommend : user={user.name}(userId={user.id})") as logger:
            logger.print(f"interest tags=({' , '.join(user.interest_tags)})")
            with WithLog("get recommends") as logger:
                recommend_results = get_recommendations(user, limit=3)
                if recommend_results is None:
                    continue
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
    except Exception as e:
        print("❌ error has occurred")
        print(e)
        print(traceback.format_exc())
        errors.append(e)

if len(errors) >= 1:
    print("通知送信時にエラーが発生しました")
    exit(1)
