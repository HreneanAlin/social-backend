import graphene
from graphene_django import DjangoObjectType
from .models import ExtendUser
from graphql_jwt.decorators import staff_member_required


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        exclude = ("password", "email")


class UsersQuery(graphene.ObjectType):
    users_by_query = graphene.List(
        UserType, query=graphene.String())
    user_by_username = graphene.Field(UserType, username=graphene.String())

    get_all_users = graphene.List(UserType)

    def resolve_users_by_query(root, info, query):
        current_user = info.context.user
        if(not query):
            return None
        user_set = set(ExtendUser.objects.filter(
            username__icontains=query).exclude(username=current_user.username))
        user_set.update(ExtendUser.objects.filter(
            first_name__icontains=query).exclude(username=current_user.username))
        user_set.update(ExtendUser.objects.filter(
            last_name__icontains=query).exclude(username=current_user.username))

        return user_set

    def resolve_user_by_username(root, info, username):
        if(not username):
            return None
        current_user = ExtendUser.objects.get(username=username)
        if(not current_user):
            return None
        return current_user

    @staff_member_required
    def resolve_get_all_users(root, info):
        return ExtendUser.objects.all()
