from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("ordered/<uuid:menu_id>", views.orders_selected_view, name="ordered"),
    path("list/", views.orders_list_view, name="list"),
]
