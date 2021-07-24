import graphene
from .events import NEW_FRIEND_REQUEST
from .graphql_types import FriendRequestType
from .models import FriendRequest


class FriendRequestSubscription(graphene.ObjectType):
    new_friend_request = graphene.Field(FriendRequestType)

    def resolve_new_friend_request(root, info):
        current_user = info.context.user
        print(current_user)
        return root.filter(
            lambda event:
                event.operation == NEW_FRIEND_REQUEST and
                isinstance(event.instance,FriendRequest ) and
                event.instance.user_to.id == current_user.id

        ).map(lambda event: event.instance)