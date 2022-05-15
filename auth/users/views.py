import re

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from oauth2_provider.decorators import protected_resource

from auth import events
from auth.events import validate_and_publish
from users.models import User

PWD = "IM_LAZY_TO_GOOGLE_HOW_TO_REMOVE_PASSWORD_FROM_USER"


def login_view(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return render(request, "users/login.html", {})
    if request.method == "POST":
        username = request.POST["username"]
        if not username:
            raise Exception

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=PWD)
            validate_and_publish(events.UserCreated_v1, user)

        user = authenticate(request, username=username, password=PWD)
        login(request, user)

        if redirect_after_login := request.GET.get("next"):
            return HttpResponseRedirect(redirect_after_login)
        return HttpResponseRedirect("/")


def logout_view(request: HttpRequest):
    redirect_url = request.GET.get("redirectUrl")
    logout(request)
    if redirect_url:
        return redirect(redirect_url)
    else:
        return HttpResponseRedirect("/")


def index_view(request: HttpRequest):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")

    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        new_username = request.POST["username"]
        if user.username != new_username:
            user.username = new_username
            user.save()
            validate_and_publish(
                events.UserUpdated_v1,
                {"public_id": user.public_id, "username": new_username},
            )
        new_role = request.POST["role"]
        if user.role != new_role:
            user.role = new_role
            user.save()
            validate_and_publish(
                events.UserUpdated_v1,
                {"public_id": user.public_id, "role": new_role},
            )
        return HttpResponseRedirect("/")

    return render(request, "users/index.html", {})


@protected_resource()
def user_info_view(request: HttpRequest):
    user = request.resource_owner
    return JsonResponse(
        {
            "username": user.username,
            "public_id": user.public_id,
            "role": user.role,
        }
    )
