from datetime import datetime, timedelta

import pytz
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils import timezone

from notifications.tasks import send_menu_notification

from .constants import OPTION_NAMES, TIME_OVER
from .forms import CreateMenu, MenuOption
from .models import MenuOptions, TodayMenu


@login_required(login_url="/employees/login/")
def menu_view(request, menu_id):
    """
    This view displays the form to select an option.
    Validates that the menu is not displays after a specific hour
    """
    if request.method == "GET":
        menu_options = MenuOptions.objects.filter(today_menu__uuid=menu_id)
        if not __is_before_end_time():
            return HttpResponseBadRequest(
                "Time is over. Try to select your option tomorrow before 11 am"
            )
        if len(menu_options) == 3:
            options = [
                (menu_options[0].id, menu_options[0].description),
                (
                    menu_options[1].id,
                    menu_options[1].description,
                ),
                (
                    menu_options[2].id,
                    menu_options[2].description,
                ),
            ]
            menu_option_form = MenuOption(options)
            return render(
                request,
                "employee/menu.html",
                {
                    "menu_options": menu_option_form,
                    "menu_id": menu_options[0].today_menu.uuid,
                    "user": request.user.username,
                    "menu_date": menu_options[0].today_menu.date,
                },
            )
        else:
            return HttpResponseBadRequest("There is no menu yet for today")


def __is_before_end_time():
    """
    Validates hour
    """
    chile = pytz.timezone("America/Santiago")
    timezone.activate(chile)
    current_date = chile.localize(datetime.utcnow())
    today_11_am = timezone.datetime(
        current_date.year,
        current_date.month,
        current_date.day,
        hour=TIME_OVER,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=chile
    ).astimezone(pytz.utc)
    print(today_11_am)
    if current_date.hour < today_11_am.hour:
        return True
    return False


@login_required(login_url="/employees/login/")
@transaction.atomic
def create_menu_view(request):
    """
    Returns a form to create a menu when the method is GET
    Save a menu into db when the method is POST
    Validates that only super-admin can be able to create the menu
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not Authorized...")

    if request.method == "POST":
        print(request.POST)
        form = CreateMenu(request.POST)
        if form.is_valid():
            today_menu_options = TodayMenu.objects.filter(
                date__year=form.cleaned_data["date"].year,
                date__month=form.cleaned_data["date"].month,
                date__day=form.cleaned_data["date"].day,
            )
            if len(today_menu_options) > 0:
                return render(
                    request,
                    "admin/create_menu.html",
                    {
                        "form": form,
                        "date_error": f"A menu for this date was already created before: {form.cleaned_data['date']}",
                    },
                )
            try:
                today_menu = TodayMenu()
                today_menu.date = form.cleaned_data["date"]
                today_menu.save()
                for option_name in OPTION_NAMES:
                    menu_option = MenuOptions()
                    menu_option.today_menu = today_menu
                    menu_option.description = form.cleaned_data[option_name]
                    menu_option.save()

                send_menu_notification.apply_async(
                    [today_menu.uuid],
                    eta=today_menu.date + timedelta(hours=8, minutes=00.0),
                )
            except Exception as exp:
                print(exp)
                transaction.set_rollback(True)
                return render(
                    request,
                    "admin/create_menu.html",
                    {"form": form, "date_error": "Data was not saved. Try again"},
                )
            return redirect("menu:create")
    else:
        form = CreateMenu()
    return render(request, "admin/create_menu.html", {"form": form})
