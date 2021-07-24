import graphene
from graphene_django import DjangoObjectType
from .models import FriendRequest


class FriendRequestType(DjangoObjectType):
    class Meta:
        model = FriendRequest
        fields = "__all__"
