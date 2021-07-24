from django.db import models
from django.db.models import constraints
from django.db.models.constraints import Deferrable
from users.models import ExtendUser
from .enums import FRIEND_REQUEST_STATUS, PENDING


class FriendRequest(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(auto_now=True)
    user_from = models.ForeignKey(
        ExtendUser, null=False, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(
        ExtendUser, null=False, on_delete=models.CASCADE, related_name='user_to')
    status = models.CharField(
        max_length=2, choices=FRIEND_REQUEST_STATUS, default=PENDING)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="Unique_friend_reques",
                fields=["user_from", "user_to"],
                deferrable=models.Deferrable.DEFERRED,
            )

        ]

    def __str__(self):
        return f'{self.id} {self.user_from.username} to {self.user_to.username}'
