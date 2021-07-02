import uuid
import pytest

from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone

from menu.models import MenuOptions, TodayMenu


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


@pytest.fixture
def menu_option_2_test(db, today_menu_test) -> MenuOptions:
    option = MenuOptions()
    option.today_menu = today_menu_test
    option.description = "Chicken Nugget Rice, Salad and Dessert"
    option.save()
    return option


@pytest.fixture
def menu_option_3_test(db, today_menu_test) -> MenuOptions:
    option = MenuOptions()
    option.today_menu = today_menu_test
    option.description = "Rice with hamburger, Salad and Dessert"
    option.save()
    return option


def test_should_get_the_form_to_create_a_menu(client, admin_user):
    client.force_login(admin_user)
    response = client.get("/menu/create/")
    assert response.status_code == 200


def test_should_get_the_form_to_menu_select(
    client, user_test, today_menu_test, menu_option_1_test, menu_option_2_test, menu_option_3_test
):
    with mock.patch('menu.views.TimeVerifier') as MockTimeVerifier:
        MockTimeVerifier.return_value.is_before_end_time.return_value = True
        client.force_login(user_test)
        client.login(username=user_test.username, password=user_test.password)
        response = client.get(f"/menu/{today_menu_test.uuid}")
        print(response.content)
        assert response.status_code == 200


def test_should_not_get_the_form_to_select_menu_and_return_bad_request(
    client, user_test, today_menu_test, menu_option_1_test, menu_option_2_test, menu_option_3_test
):
    with mock.patch('menu.views.TimeVerifier') as MockTimeVerifier:
        MockTimeVerifier.return_value.is_before_end_time.return_value = False
        client.force_login(user_test)
        client.login(username=user_test.username, password=user_test.password)
        response = client.get(f"/menu/{today_menu_test.uuid}")
        print(response.content)
        assert response.status_code == 400
        assert response.content.decode("utf-8") == "Time is over. Try to select your option tomorrow before 11 am"


def test_should_not_get_the_form_to_select_menu_no_menu_yet(client, user_test):
    message = "There is no menu yet for today"
    with mock.patch('menu.views.TimeVerifier') as MockTimeVerifier:
        MockTimeVerifier.return_value.is_before_end_time.return_value = True
        client.force_login(user_test)
        client.login(username=user_test.username, password=user_test.password)
        response = client.get(f"/menu/{str(uuid.uuid4())}")
        assert message in response.content.decode("utf-8")
        assert response.status_code == 400


def test_should_not_get_the_form_to_create_a_menu_no_admin_ser(client, user_test):
    client.force_login(user_test)
    client.login(username=user_test.username, password=user_test.password)
    response = client.get('/menu/create/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_should_create_a_menu_admin_ser(client, admin_user):
    client.force_login(admin_user)
    client.login(username=admin_user.username, password=admin_user.password)
    response = client.post('/menu/create/', {
        "date": "2021-07-02",
        "option1": "example",
        "option2": "example2",
        "option3": "example3",
    })

    today_menu = TodayMenu.objects.all()
    options = MenuOptions.objects.all()
    assert len(today_menu) == 1
    assert len(options) == 3
    assert options[0].description == "example"
    assert options[1].description == "example2"
    assert options[2].description == "example3"
    assert response.status_code == 302
