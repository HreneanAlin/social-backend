import graphene
from graphene_django import DjangoObjectType
from .models import Post, PostImage, PostComment

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

class PostImageType(DjangoObjectType):
    class Meta:
        model = PostImage
        fields = "__all__"

class PostCommentType(DjangoObjectType):
    class Meta:
        model = PostComment
        fields = "__all__"