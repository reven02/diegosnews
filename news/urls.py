from django.urls import path

from . import views

urlpatterns = [
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("stories", views.stories, name="stories"),
    path("stories/<int:key>", views.delete_story, name="delete_stories"),
]