import uuid

from django.db import models


class TodayMenu(models.Model):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    date = models.DateTimeField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.uuid} menu date: {self.date}"


class MenuOptions(models.Model):
    description = models.TextField()
    today_menu = models.ForeignKey(TodayMenu, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ["created"]
