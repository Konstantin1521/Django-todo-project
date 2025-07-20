from django.contrib import admin

# Register your models here.
from todo_list.models import ToDoItem

@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = "id", "title", "done"
    list_display_links = "id", "title"

    def __str__(self) -> str:
        return self.title