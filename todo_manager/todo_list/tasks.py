import logging
import pika
from celery import shared_task
from .models import ToDoItem

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, retry_backoff=True)
def send_task_reminder(self, task_id, chat_id=None):
    """
    Отправляет напоминание о задаче в RabbitMQ для Telegram-бота.

    Args:
        task_id (int): ID задачи в базе.
        chat_id (str, optional): ID чата для отправки в Telegram.
    """
    try:
        task = ToDoItem.objects.get(id=task_id)
        if task.done:
            logger.info(f"Task {task_id} ({task.title}) already done, skipping notification.")
            return None  # Явный возврат для Celery

        # Экранирование для защиты от XSS/injection
        safe_title = task.title.replace('<', '&lt;').replace('>', '&gt;')
        message = {
            'chat_id': 682375933,  # Предполагается telegram_id в модели User
            'text': f"Напоминание: задача '{safe_title}' должна быть выполнена до {task.execute_time}!"
        }

        # Синхронная публикация в RabbitMQ через pika
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('guest_dj', 'guest_dj')
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='notifications', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='notifications',
            body=str(message).encode(),
            properties=pika.BasicProperties(delivery_mode=2)  # Устойчивая доставка
        )
        connection.close()

        logger.info(f"Notification sent for task {task_id} to chat_id {message['chat_id']}.")
        return message  # Возврат сериализуемого результата

    except ToDoItem.DoesNotExist:
        logger.error(f"Task with ID {task_id} not found.")
        raise self.retry(countdown=60)
    except Exception as e:
        logger.error(f"Error in send_task_reminder for task {task_id}: {str(e)}")
        raise self.retry(exc=e, countdown=60)