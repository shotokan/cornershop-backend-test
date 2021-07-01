from django.contrib.auth.models import User
from django.db import models

from menu.models import MenuOptions, TodayMenu


class Orders(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(TodayMenu, on_delete=models.CASCADE)
    option_selected = models.ForeignKey(
        MenuOptions, on_delete=models.CASCADE, null=True
    )
    customizations = models.CharField(max_length=150)
    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = [["employee", "menu"]]
