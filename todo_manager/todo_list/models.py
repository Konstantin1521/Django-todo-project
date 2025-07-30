import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse

from django.utils import timezone
class ToDoGroup(models.Model):
    class Meta:
        ordering = ("id", "name", "owner")
        verbose_name = "Group"

        constraints = [UniqueConstraint(
            fields=["owner","name"],
            name="unique_together"
        )]

    name = models.CharField(max_length=70)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    tg_id = models.BigIntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    verification_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    verified = models.BooleanField(default=False)


    def generate_verification_code(self):
        """Генерирует уникальный код верификации."""
        for _ in range(10):
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not TelegramProfile.objects.filter(verified_code=code).exists():
                return code
        raise ValueError("Не удалось сгенерировать уникальный код верификации.")

    def __str__(self):
        return self.user.username if self.user else "No user"

    class Meta:
        verbose_name = "Telegram Profile"
        ordering = ("-created_at",)


# Create your models here.
class ToDoItem(models.Model):
    class Meta:
        ordering = ("id",)
        verbose_name = "ToDo"

    title = models.CharField(max_length=70)
    description = models.TextField(max_length=250, null=True, blank=True)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    execute_time = models.DateTimeField(default=timezone.now)
    remind_before = models.IntegerField(default=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    group = models.ForeignKey(ToDoGroup, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")

    def get_absolute_url(self):
        return reverse(
            "todo_list:detail",
            kwargs={"pk": self.pk},
        )

    def __str__(self):
        return self.title