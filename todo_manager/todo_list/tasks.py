from celery import shared_task
from .models import ToDoItem

@shared_task
def send_task_reminder(task_id):
    try:
        task = ToDoItem.objects.get(id=task_id)
        if not task.done:
            print(f"Напоминание: задача '{task.title}' скоро должна быть выполнена!")
        else:
            print(f"Задача {task.title} уже выполнена — уведомление не отправляется.")
    except ToDoItem.DoesNotExist:
        print(f"Задача с ID {task_id} не найдена")
