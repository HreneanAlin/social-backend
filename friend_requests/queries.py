import graphene
from .graphql_types import FriendRequestType
from .models import FriendRequest
from .enums import PENDING
from users.models import ExtendUser


class FriendRequestQuery(graphene.ObjectType):
    my_friend_requests = graphene.List(FriendRequestType)
    check_user_relation = graphene.String(username=graphene.String())

    def resolve_my_friend_requests(root, info):
        current_user = info.context.user
        qs = FriendRequest.objects.filter(
            user_to__username=current_user.username).filter(status=PENDING)
        return qs

    def resolve_check_user_relation(root, info, username):
        current_user = info.context.user
        qs = FriendRequest.objects.filter(
            user_to=current_user).filter(user_from__username=username)
        if(qs.exists()):
            friendRequest = qs[0]
            return friendRequest.status
        else:
            qs = FriendRequest.objects.filter(
                user_from=current_user).filter(user_to__username=username)
            if(qs.exists()):
                friendRequest = qs[0]
                return f'M{friendRequest.status}'
            else:
                return 'N'
