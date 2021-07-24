from posts.models import Post
import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from users.schema import AuthMutation
from users.queries import UsersQuery
from temporary_images.schema import TemporaryImageMutation
from posts.queries import PostQuery
from posts.mutations import PostMutation
from posts.subscriptions import PostsSubscription
from friend_requests.mutations import FriendRequestMutation
from friend_requests.queries import FriendRequestQuery
from friend_requests.subscriptions import FriendRequestSubscription


class Mutation(PostMutation, AuthMutation, TemporaryImageMutation, FriendRequestMutation, graphene.ObjectType):
    pass


class Query(PostQuery, UsersQuery, MeQuery, FriendRequestQuery, graphene.ObjectType):
    pass


class Subscription(PostsSubscription,FriendRequestSubscription):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)
