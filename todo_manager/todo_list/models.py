from django.db import models
from django.urls import reverse


# Create your models here.
class ToDoItem(models.Model):
    class Meta:
        ordering = ("id",)
        verbose_name = "ToDo name"

    title = models.CharField(max_length=70)
    description = models.TextField(max_length=250, null=True, blank=True)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "todo_list:detail",
            kwargs={"pk": self.pk},
        )
