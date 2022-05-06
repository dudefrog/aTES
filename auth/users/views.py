import re

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource

from auth.async_messaging import UserLoggedIn, UsernameChanged, UserRegistered
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
            UserRegistered(user).send()

        user = authenticate(request, username=username, password=PWD)
        login(request, user)
        UserLoggedIn(user).send()

        if redirect_after_login := request.GET.get("next"):
            return HttpResponseRedirect(redirect_after_login)
        return HttpResponseRedirect("/")


def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect("/")


def index_view(request: HttpRequest):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")

    if request.method == "POST":
        new_username = request.POST["username"]
        user = User.objects.get(id=request.user.id)
        user.username = new_username
        user.save()
        UsernameChanged(user).send()
        return HttpResponseRedirect("/")

    return render(request, "users/index.html", {})


@protected_resource()
def user_info_view(request: HttpRequest):
    user = request.resource_owner
    return JsonResponse(
        {
            "username": user.username,
            "user_id": user.id,
        }
    )
