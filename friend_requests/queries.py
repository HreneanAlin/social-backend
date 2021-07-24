import graphene
from .graphql_types import FriendRequestType
from .models import FriendRequest

class FriendRequestQuery(graphene.ObjectType):
    my_friend_requests = graphene.List(FriendRequestType)

    def resolve_my_friend_requests(root,info):
        current_user = info.context.user
        qs = FriendRequest.objects.filter(user_to__username=current_user.username)
        print(qs)
        return qs
        
