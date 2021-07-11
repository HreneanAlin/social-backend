from django.db import models

# Create your models here.

def upload_path(instance,filename):
    return '/'.join(['temporaryImages',filename])

class TemporaryImage(models.Model):
    image = models.ImageField(upload_to=upload_path)


    def __str__(self):
        return self.image.name