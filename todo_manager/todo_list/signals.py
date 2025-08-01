from django.db.models.signals import post_save
from django.dispatch import receiver
from todo_list.models import ToDoGroup
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_default_group(sender, instance, created, **kwargs):
    if created:
        ToDoGroup.objects.get_or_create(name="Без группы", owner=instance)