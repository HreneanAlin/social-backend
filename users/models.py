from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_path(instance,filename):
    return '/'.join(['profilePictures',str(instance.id),filename])

def upload_path_cover(instance,filename):
    return '/'.join(['cover_Pictures',str(instance.id),filename])


class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False,max_length=255,verbose_name='email')
    country = models.CharField(max_length=255,verbose_name='country',blank=False)
    profile_picture = models.ImageField(upload_to=upload_path)
    my_test = models.CharField(max_length=255,verbose_name='my_test',blank=True)
    friends = models.ManyToManyField("ExtendUser",blank=True)
    declined_friends = models.ManyToManyField("ExtendUser",blank=True,related_name="declined")
    cover_image = models.ImageField(upload_to=upload_path_cover,default='default_cover.jpeg')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

ExtendUser._meta.get_field('first_name').blank = False
ExtendUser._meta.get_field('first_name').null = False
ExtendUser._meta.get_field('last_name').blank = False
ExtendUser._meta.get_field('last_name').null = False
