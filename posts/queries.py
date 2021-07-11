import graphene
# from rx import Observable
from graphene_django import DjangoObjectType
from .models import Post, PostImage, PostComment
from .graphql_types import PostType, PostImage, PostCommentType



class PostQuery(graphene.ObjectType):
    my_posts = graphene.List(PostType)
    posts_by_username = graphene.List(PostType,username=graphene.String())
    comments_by_post = graphene.List(PostCommentType,post_id=graphene.Int(required=True))

    def resolve_my_posts(root,info):
        current_user = info.context.user
        return None
    
    def resolve_posts_by_username(root,info,username):
        return Post.objects.filter(user__username=username)
    
    def resolve_comments_by_post(root,info,post_id):
        return PostComment.objects.filter(post__id=post_id)