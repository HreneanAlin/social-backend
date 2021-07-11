import graphene
from django.utils.module_loading import import_string
from django import forms
from django.db import transaction
from smtplib import SMTPException
from graphql_auth import mutations
from graphql_auth.mixins import UserModel
from graphql_auth.models import UserStatus
from graphql_auth.signals import user_registered
from graphql_auth.exceptions import EmailAlreadyInUse
from graphql_auth.constants import Messages
from graphql_auth.settings import graphql_auth_settings as app_settings
from graphene_file_upload.scalars import Upload
from django.contrib.auth import get_user_model

if app_settings.EMAIL_ASYNC_TASK and isinstance(app_settings.EMAIL_ASYNC_TASK, str):
    async_email_func = import_string(app_settings.EMAIL_ASYNC_TASK)
else:
    async_email_func = None


class CostumeRegister(mutations.Register):
    class Arguments:
        profile_picture = Upload(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                f = cls.form(kwargs)
                if f.is_valid():
                    email = kwargs.get(UserModel.EMAIL_FIELD, False)
                    UserStatus.clean_email(email)
                    user = f.save()
                    profile_pic = kwargs['profile_picture']
                    user.profile_picture = profile_pic
                    user.save()
                    send_activation = (
                        app_settings.SEND_ACTIVATION_EMAIL is True and email
                    )
                    send_password_set = (
                        app_settings.ALLOW_PASSWORDLESS_REGISTRATION is True
                        and app_settings.SEND_PASSWORD_SET_EMAIL is True
                        and email
                    )
                    if send_activation:
                        if async_email_func:
                            async_email_func(
                                user.status.send_activation_email, (info,))
                        else:
                            user.status.send_activation_email(info)

                    if send_password_set:
                        if async_email_func:
                            async_email_func(
                                user.status.send_password_set_email, (info,)
                            )
                        else:
                            user.status.send_password_set_email(info)

                    user_registered.send(sender=cls, user=user)

                    if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
                        payload = cls.login_on_register(
                            root, info, password=kwargs.get("password1"), **kwargs
                        )
                        return_value = {}
                        for field in cls._meta.fields:
                            return_value[field] = getattr(payload, field)
                        return cls(**return_value)
                    return cls(success=True)
                else:
                    return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(
                success=False,
                errors={UserModel.EMAIL_FIELD: Messages.EMAIL_IN_USE},
            )
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
