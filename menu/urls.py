from django.urls import path

from . import views

app_name = "menu"

urlpatterns = [
    path("<uuid:menu_id>", views.menu_view, name="select"),
    path("create/", views.create_menu_view, name="create"),
]
