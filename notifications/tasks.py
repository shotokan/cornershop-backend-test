from celery.task import task
from celery.utils.log import get_task_logger

from .notification_service import NotificationService
from .slack_client import SlackWrapper

logger = get_task_logger(__name__)


@task(name="send_menu_notification")
def send_menu_notification(menu_id):
    """
    This functions is used as a celery task to sent a notification through celery
    """
    logger.info("sending...")
    slack_client = SlackWrapper()
    notification = NotificationService(slack_client)
    notification.send_message(menu_id)
    return True
