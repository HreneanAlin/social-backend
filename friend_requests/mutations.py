import graphene
from users.models import ExtendUser
from graphene_subscriptions.events import SubscriptionEvent
from .models import FriendRequest
from .events import NEW_FRIEND_REQUEST


class SendFriendRequest(graphene.Mutation):

    class Arguments:
        username = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, username):
        try:
            current_user = info.context.user
            user_to_send = ExtendUser.objects.get(username=username)
            friend_request = FriendRequest(
                user_from=current_user, user_to=user_to_send)
            friend_request.save()
            print("id1 ",friend_request.user_to.username)
            event = SubscriptionEvent(operation=NEW_FRIEND_REQUEST,instance=friend_request)
            event.send()
            return SendFriendRequest(success=True)
        except:
            return SendFriendRequest(success=False)



class FriendRequestMutation(graphene.ObjectType):
    send_friend_request = SendFriendRequest.Field()