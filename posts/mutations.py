import graphene
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from .models import Post,PostImage, PostComment
from graphene_subscriptions.events import SubscriptionEvent
from .events import NEW_POST_COMMENT
class ImageDescType(graphene.InputObjectType):
    description = graphene.String()
    file = Upload()

class AddPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        images = graphene.List(ImageDescType)
    
    success = graphene.Boolean()
 


    @classmethod
    def mutate(cls,root,info,title,text,images):
        try:
            current_user = info.context.user
            post = Post(user=current_user,title=title,text=text)
            post.save()
            if images:
                for obj in images:
                    post_image = PostImage(post=post,title=obj.description,image=obj.file)
                    post_image.save()
        
            return AddPost(success = True)
        except:
            return AddPost(success = False)


class AddCommentPost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        comment_text = graphene.String(required=True)
    
    success = graphene.Boolean()

    @classmethod
    def mutate(cls,root,info,post_id,comment_text):
        try:
            current_user = info.context.user
            current_post = Post.objects.get(id=post_id)
            comment = PostComment(user=current_user,text=comment_text,post=current_post)
            comment.save()
            event = SubscriptionEvent(operation=NEW_POST_COMMENT,instance=comment)
            event.send()
            return AddCommentPost(success = True)
        except:
            return AddCommentPost(success = False)


class PostMutation(graphene.ObjectType):
    add_post= AddPost.Field()
    add_comment_post = AddCommentPost.Field()