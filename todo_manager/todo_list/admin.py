from django.contrib import admin

# Register your models here.
from todo_list.models import ToDoItem, ToDoGroup, TelegramProfile


@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = "id", "title", "archived", "done"
    list_display_links = "id", "title"

    def visible(self, obj: ToDoItem) -> bool:
        return obj.archived

    visible.boolean = True

    def __str__(self) -> str:
        return self.title


@admin.register(ToDoGroup)
class ToDoGroupAdmin(admin.ModelAdmin):
    list_display = "id", "name", "owner"
    list_display_links = "id", "name"



@admin.register(TelegramProfile)
class ToDoGroupAdmin(admin.ModelAdmin):
    list_display = "user", "tg_id",
    list_display_links = "user", "tg_id"