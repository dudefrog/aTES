from statistics import mode

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # this field should be required, but otherwise createsuperuser will fail
    external_user_id = models.IntegerField(null=True)
