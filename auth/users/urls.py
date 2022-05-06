from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user-info/", views.user_info_view, name="user-info"),
]