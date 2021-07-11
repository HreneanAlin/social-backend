from django.contrib import admin
from .models import Post, PostImage, PostComment

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostComment)

