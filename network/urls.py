
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("likes", views.likes, name="likes"),
]
