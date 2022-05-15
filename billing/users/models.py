from django.contrib.auth.models import AbstractUser
from django.db import models

PWD = "IM_LAZY_TO_GOOGLE_HOW_TO_REMOVE_PASSWORD_FROM_USER"


class User(AbstractUser):
    # this field should be required, but otherwise createsuperuser will fail
    public_id = models.CharField(null=True, max_length=64, editable=False)
    role = models.CharField(default="user", max_length=50)

    balance = models.IntegerField(default=0)
