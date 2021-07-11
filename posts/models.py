from django.db import models
from users.models import ExtendUser


def upload_path(instance, filename):
    return '/'.join(['PostImages', str(instance.post.user.username), filename])


class Post(models.Model):
    user = models.ForeignKey(ExtendUser, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + str(self.id)


class PostImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=False, upload_to=upload_path)
    post = models.ForeignKey(Post, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title

class PostComment(models.Model):
    user = models.ForeignKey(ExtendUser, null=False, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    post = models.ForeignKey(Post, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.post.title}'