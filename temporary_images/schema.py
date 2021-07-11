import graphene
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from .models import TemporaryImage


class TemporaryImageType(DjangoObjectType):
    class Meta:
        model = TemporaryImage
        fields = ("id", "image")

class AddTemporaryImage(graphene.Mutation):
    class Arguments:
        image = Upload(required=True)
    
    temp_image = graphene.Field(TemporaryImageType)

    @classmethod
    def mutate(cls,root,info,image):
        print(image)
        temporary_image = TemporaryImage(image=image)
        temporary_image.save()
        return AddTemporaryImage(temp_image=temporary_image)


class TemporaryImageMutation(graphene.ObjectType):
    add_image = AddTemporaryImage.Field()