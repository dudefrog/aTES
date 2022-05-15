from .models import PWD, User


def get_or_create_user(public_id: str, username: str = "popug", role: str = ""):
    try:
        return User.objects.get(public_id=public_id)
    except User.DoesNotExist:
        return User.objects.create_user(
            username=username,
            password=PWD,
            public_id=public_id,
            role=role,
        )
