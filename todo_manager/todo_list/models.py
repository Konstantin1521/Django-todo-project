from django.db import models

# Create your models here.
class ToDoItem(models.Model):
    class Meta:
        ordering = ("id",)
        verbose_name = "ToDo name"

    title = models.CharField(max_length=70)
    description = models.TextField(max_length=250, null=True, blank=True)
    done = models.BooleanField(default=False)
