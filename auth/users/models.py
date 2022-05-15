import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def make_uuid4():
    return str(uuid.uuid4())


class User(AbstractUser):
    role = models.CharField(default="user", max_length=64)
    public_id = models.CharField(default=make_uuid4, max_length=64, editable=False)
