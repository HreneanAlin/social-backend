import graphene
from users.models import ExtendUser
from graphene_subscriptions.events import SubscriptionEvent
from .models import FriendRequest
from .events import NEW_FRIEND_REQUEST
from .enums import ACCEPTED, PENDING, DECLINED


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
            print("id1 ", friend_request.user_to.username)
            event = SubscriptionEvent(
                operation=NEW_FRIEND_REQUEST, instance=friend_request)
            event.send()
            return SendFriendRequest(success=True)
        except:
            return SendFriendRequest(success=False)


class AcceptFriendRequest(graphene.Mutation):

    class Arguments:
        friend_request_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, friend_request_id):
        try:
            current_user = info.context.user
            friend_request = FriendRequest.objects.filter(
                user_to=current_user).filter(status=PENDING).get(id=friend_request_id)
            friend_request.status = ACCEPTED
            friend_request.save()
            current_user.friends.add(friend_request.user_from)
            current_user.save()
            print(friend_request)
            return AcceptFriendRequest(success=True)
        except:
            return SendFriendRequest(success=False)


class FriendRequestMutation(graphene.ObjectType):
    send_friend_request = SendFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
