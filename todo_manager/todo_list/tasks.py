# todo_list/tasks.py

from celery import shared_task
from django.contrib.auth import get_user_model

@shared_task
def send_notification(user_id, message):
    user = get_user_model().objects.get(id=user_id)
    print(f"📬 Sending message to {user.username}: {message}")
