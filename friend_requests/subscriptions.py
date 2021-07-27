import graphene
from .events import NEW_FRIEND_REQUEST
from .graphql_types import FriendRequestType
from .models import FriendRequest


class FriendRequestSubscription(graphene.ObjectType):
    new_friend_request = graphene.Field(FriendRequestType, username=graphene.String())

    def resolve_new_friend_request(root, info, username):
        current_user = info.context.user
        print("current ",current_user)
        return root.filter(
            lambda event:
                event.operation == NEW_FRIEND_REQUEST and
                isinstance(event.instance,FriendRequest ) and
                event.instance.user_to.username == username

        ).map(lambda event: event.instance)