from posts.models import Post
import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from users.schema import AuthMutation
from users.queries import UsersQuery
from temporary_images.schema import TemporaryImageMutation
from posts.queries import PostQuery
from posts.mutations import PostMutation



class Mutation(PostMutation, AuthMutation,TemporaryImageMutation,graphene.ObjectType):
    pass

class Query(PostQuery,UsersQuery, MeQuery, graphene.ObjectType):
    pass


class Subscription(PostQuery):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation,subscription=Subscription)