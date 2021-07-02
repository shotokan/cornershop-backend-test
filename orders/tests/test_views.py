import uuid

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from menu.models import MenuOptions, TodayMenu
from orders.models import Orders


@pytest.fixture
def user_test(db, django_user_model) -> User:
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    return user


@pytest.fixture
def today_menu_test(db) -> TodayMenu:
    today_menu = TodayMenu()
    today_menu.uuid = uuid.uuid4()
    today_menu.date = timezone.now()
    today_menu.save()
    return today_menu


@pytest.fixture
def menu_option_1_test(db, today_menu_test) -> MenuOptions:
    option = MenuOptions()
    option.today_menu = today_menu_test
    option.description = "Corn pie, Salad and Dessert"
    option.save()
    return option


def test_should_list_orders_when_employee_is_authenticated(client, user_test):
    username = "user1"
    password = "bar"
    client.force_login(user_test)
    client.login(username=username, password=password)
    response = client.get("/orders/list/")
    assert response.status_code == 200


def test_should_redirect_to_login_when_user_is_not_authenticated_order_list_view(
    client,
):
    response = client.get("/orders/list/")
    assert response.status_code == 302
    assert response.url == "/employees/login/?next=/orders/list/"


@pytest.mark.django_db
def test_should_create_a_new_order_ordered_view_with_valid_data(
    client, user_test, today_menu_test, menu_option_1_test
):
    username = "user1"
    password = "bar"
    customizations = "all is good"
    client.force_login(user_test)
    client.login(username=username, password=password)
    response = client.post(
        f"/orders/ordered/{today_menu_test.uuid}",
        {
            "option": menu_option_1_test.id,
            "customizations": customizations,
        },
    )
    orders = Orders.objects.all()
    assert len(orders) == 1
    assert orders[0].employee.username == username
    assert orders[0].option_selected.description == menu_option_1_test.description
    assert response.status_code == 302
    assert response.url == "/orders/list/"


@pytest.mark.django_db
def test_should_redirect_to_update_values_when_invalid_data(
    client, user_test, today_menu_test
):
    username = "user1"
    password = "bar"
    client.force_login(user_test)
    client.login(username=username, password=password)
    response = client.post(
        f"/orders/ordered/{today_menu_test.uuid}",
        {
            "customizations": "all is good",
            "csrfmiddlewaretoken": "go90mnciw6eTMiXTs8wWPEVNzFe6uIkDhSfswoIK8QmpV70QPZ44vQqt1I4fcATo",
        },
    )
    orders = Orders.objects.all()
    assert len(orders) == 0
    assert response.status_code == 302
    assert response.url == f"/menu/{today_menu_test.uuid}"


@pytest.mark.django_db
def test_should_return_400_ordered_view_get(client, user_test, today_menu_test):
    username = "user1"
    password = "bar"
    client.force_login(user_test)
    client.login(username=username, password=password)
    response = client.get(f"/orders/ordered/{today_menu_test.uuid}")
    orders = Orders.objects.all()
    assert len(orders) == 0
    assert response.status_code == 400
    assert response.content.decode("utf-8") == "Order was not registered"
