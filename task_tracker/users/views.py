import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from task_tracker import settings
from users.models import User

PWD = "IM_LAZY_TO_GOOGLE_HOW_TO_REMOVE_PASSWORD_FROM_USER"
CALLBACK_URL = f"{settings.BASE_URL}/oauth/callback"


def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "users/login.html", {})
    if request.method == "POST":
        url = (
            f"{settings.OAUTH_PROVIDER_BASE_URL}/o/authorize/"
            f"?client_id={settings.OAUTH_CLIENT_ID}"
            f"&redirect_uri={CALLBACK_URL}"
            "&response_type=code"
        )
        return HttpResponseRedirect(url)


def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect("/login")


def oauth_callback(request: HttpRequest):
    code = request.GET["code"]
    resp = requests.post(
        f"{settings.OAUTH_PROVIDER_BASE_URL}/o/token/",
        data={
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": CALLBACK_URL,
        },
    )

    if resp.ok:
        resp_data = resp.json()
        access_token = resp_data["access_token"]
        refresh_token = resp_data["refresh_token"]
        user_info_resp = requests.get(
            "http://localhost:5000/user-info",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if user_info_resp.ok:
            user_info = user_info_resp.json()
            username = user_info["username"]
            try:
                User.objects.get(external_user_id=user_info["user_id"])
            except User.DoesNotExist:
                User.objects.create_user(
                    username=username,
                    external_user_id=user_info["user_id"],
                    password=PWD,
                )
            user = authenticate(request, username=username, password=PWD)
            login(request, user)
            return HttpResponseRedirect("/")

    return render(request, "users/login.html", {})
