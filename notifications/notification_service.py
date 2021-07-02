from django.conf import settings

from .slack_client import SlackWrapper


DOMAIN = getattr(settings, "PROJECT_DOMAIN", "http://localhost:8000")


class NotificationService:
    """
    This class is a service to be able to send a notification
    """
    def __init__(self):
        self.__slack_client = SlackWrapper()

    def send_message(self, menu_id):
        """
        Sends a notification to slack
        """
        users = self.__slack_client.get_users()
        for user in users:
            message = f"Hello, {user.username}!, see today's menu {DOMAIN}/menu/select/{menu_id}"
            self.__slack_client.send_message(user, message)
