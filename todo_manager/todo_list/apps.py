from django.apps import AppConfig


class TodoListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_list'
    verbose_name = "ToDo List"

    def ready(self):
        import todo_list.signals
