from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from todo_list.models import ToDoGroup
from django.contrib.auth.models import User

#
@receiver(post_migrate)
def create_default_group(sender, **kwargs):
    default_user, created = User.objects.get_or_create(
        username='Admin',
        defaults={
            'is_staff': True,
            'is_superuser': True,
        }
    )

    if created:
        default_user.set_password('Admin')
        default_user.save()

    ToDoGroup.objects.get_or_create(
        name='Без группы',
        defaults={'owner': default_user}
    )

@receiver(post_save, sender=User)
def create_default_group(sender, instance, created, **kwargs):
    if created:
        ToDoGroup.objects.get_or_create(name="Без группы", owner=instance)