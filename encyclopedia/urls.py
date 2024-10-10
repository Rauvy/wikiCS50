from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.get_entry, name="get_entry"),
    path("newentry", views.new_page, name="new_page"),
    path("get_random_entry", views.get_random_entry, name="get_random_entry"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>/edit", views.edit_entry, name="edit_entry")
]
