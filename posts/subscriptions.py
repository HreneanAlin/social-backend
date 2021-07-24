import graphene
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import CREATED
from .graphql_types import PostCommentType
from .models import PostComment
from .events import NEW_POST_COMMENT



class PostsSubscription(graphene.ObjectType):
    new_post_comment = graphene.Field(PostCommentType,post_id=graphene.Int(required=True))

    def resolve_new_post_comment(root,info,post_id):
         print("the root",root)
         return root.filter(
            lambda event:
                event.operation == NEW_POST_COMMENT and
                isinstance(event.instance, PostComment) and
                event.instance.post.id == post_id

        ).map(lambda event: event.instance)