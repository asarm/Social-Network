
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("editPost/<int:pk>", views.editPost, name="editPost"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("followings", views.following_view, name="followings"),
    path("reach_error", views.error, name="error"),
    url(r'^likepost/$', views.like_post, name='like-post')
]
