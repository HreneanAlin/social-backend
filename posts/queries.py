import graphene
# from rx import Observable
from graphene_django import DjangoObjectType
from .models import Post, PostImage, PostComment
from .graphql_types import PostType, PostImage, PostCommentType
from rx import Observable
from graphene_subscriptions.events import CREATED

class PostPagination(graphene.ObjectType):
    hasNext = graphene.Boolean()
    posts_by_username = graphene.List(
        PostType)


class CommentPagination(graphene.ObjectType):
    hasNext = graphene.Boolean()
    comments_by_post = graphene.List(PostCommentType)


class PostQuery(graphene.ObjectType):
    hello = graphene.String()
    my_posts = graphene.List(PostType)
    posts_by_username_pagination = graphene.Field(PostPagination, username=graphene.String(
    ), first=graphene.Int(), skip=graphene.Int(required=False))
    comments_by_post = graphene.List(
        PostCommentType, post_id=graphene.Int(required=True))
    comments_by_post_pagination = graphene.Field(CommentPagination, post_id=graphene.Int(
    ), first=graphene.Int(), skip=graphene.Int(required=False))

    def resolve_my_posts(root, info):
        current_user = info.context.user
        return None

    def resolve_posts_by_username_pagination(root, info, username, first=10, skip=0, **kwargs):
        hasNext = True
        qs = Post.objects.filter(user__username=username).order_by("-id")
        qs = qs[skip:]
        qs = qs[:first]
        if len(qs) < first:
            hasNext = False

        return PostPagination(posts_by_username=qs, hasNext=hasNext)

    def resolve_comments_by_post(root, info, post_id):
        return PostComment.objects.filter(post__id=post_id)

    def resolve_comments_by_post_pagination(root, info, post_id, first=10, skip=0, **kwargs):
        hasNext = True
        qs = PostComment.objects.filter(post__id=post_id).order_by("-id")
        qs = qs[skip:]
        qs = qs[:first]
        if len(qs) < first:
            hasNext = False
        return CommentPagination(comments_by_post=qs, hasNext=hasNext)

    def resolve_hello(root, info):
        return Observable.interval(3000) \
            .map(lambda i: "hello world!")
