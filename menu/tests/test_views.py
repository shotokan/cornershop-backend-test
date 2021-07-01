import uuid
from datetime import datetime

import pytest

from django.contrib.auth.models import User
from django.utils import timezone

import menu.constants
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


def test_should_get_the_form_to_create_a_menu(client, admin_user):
    client.force_login(admin_user)
    response = client.get("/menu/create/")
    assert response.status_code == 200


def test_should_get_the_form_to_menu_select(
    client, admin_user, today_menu_test, menu_option_1_test
):
    client.force_login(admin_user)
    print('uuid', today_menu_test.uuid)
    menu.constants.TIME_OVER = 8
    response = client.get(f"/menu/select/{today_menu_test.uuid}/")
    assert response.status_code == 200


def test_should_not_get_the_form_to_create_a_menu_no_admin_ser(client, user_test):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get('/menu/create/')
    assert response.status_code == 403
