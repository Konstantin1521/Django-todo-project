from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse


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


# Create your models here.
class ToDoItem(models.Model):
    class Meta:
        ordering = ("id",)
        verbose_name = "ToDo"

    title = models.CharField(max_length=70)
    description = models.TextField(max_length=250, null=True, blank=True)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    group = models.ForeignKey(ToDoGroup, on_delete=models.CASCADE, null=True, blank=True,)

    def get_absolute_url(self):
        return reverse(
            "todo_list:detail",
            kwargs={"pk": self.pk},
        )

    def __str__(self):
        return self.title