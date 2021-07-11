# from django.db.models.signals import post_save, post_delete
# from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription
# from django.apps import AppConfig
# from posts.models import PostComment

# post_save.connect(post_save_subscription, sender=PostComment, dispatch_uid="PostComment_post_save")


# class CoreAppConfig(AppConfig):
#     name = 'your_app'

#     def ready(self):
#         import core.signals