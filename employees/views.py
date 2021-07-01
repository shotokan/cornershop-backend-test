from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def signup_view(request):
    """
    Returns a form when the method is GET and validates and save a user when the
    method is POST
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect("menu:menu")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """
    Returns a form to login and when the method is POST validates the form
    and the user to generate a session and redirect to a new url
    """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in the user
            user = form.get_user()
            login(request, user)
            if request.user.is_superuser:
                return redirect("menu:create")
            return redirect(request.POST.get("next", "orders:list"))
    else:
        form = AuthenticationForm()
    return render(
        request, "accounts/login.html", {"form": form, "next": request.GET.get("next")}
    )


def logout_view(request):
    """
    Log out the user using logout funtion from django
    """
    logout(request)
    return redirect("employees:login")
