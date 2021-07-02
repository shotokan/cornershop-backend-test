from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from menu.models import MenuOptions, TodayMenu
from orders.forms import SelectOption
from orders.models import Orders


@login_required(login_url="/employees/login/")
def orders_selected_view(request, menu_id):
    """Saves the selected option from de menu into the db.
    parameters:
        request: django object
        menu_id: an uuid that identifies a menu in db
    returns:
        HttpResponseBadRequest: response a bad request code and message
        redirect: redirect to see a list of menus that has been selected by user
    """
    if request.method == "POST":
        form = SelectOption(request.POST)
        if form.is_valid():
            #TODO: Here needs to be validated the limitation time to be able to select an option
            new_order = Orders()
            today_menu = TodayMenu.objects.get(uuid=menu_id)
            option_selected = MenuOptions.objects.get(pk=form.cleaned_data["option"])
            new_order.employee = request.user
            new_order.menu = today_menu
            new_order.option_selected = option_selected
            new_order.customizations = form.cleaned_data["customizations"]
            new_order.save()
            return redirect("orders:list")
        else:
            return redirect("menu:select", menu_id=menu_id)
    else:
        return HttpResponseBadRequest("Order was not registered")


@login_required(login_url="/employees/login/")
def orders_list_view(request):
    """List all options that a employee has selected
    parameters:
        request: django object
        render: a web page that displays the orders or option that belong to the employee
    """
    orders = Orders.objects.filter(employee__id=request.user.id)
    date = datetime.utcnow()
    today_menu = TodayMenu.objects.filter(
        date__year=date.year, date__month=date.month, date__day=date.day
    )
    menu_uuid = today_menu[0].uuid if len(today_menu) > 0 else None
    return render(
        request,
        "employee/orders.html",
        {"orders": orders, "menu_uuid": menu_uuid, "user": request.user.username},
    )
