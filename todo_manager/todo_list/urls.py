
from django.urls import path

from . import views_dir

app_name = "todo_list"

urlpatterns = [
    path('', views_dir.todoGroupView.ToDoGroupWithTasksIndexView.as_view(), name="index"),
    path('<int:pk>/', views_dir.todoTaskView.ToDoDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', views_dir.todoTaskView.ToDoItemUpdateView.as_view(), name="update"),
    path('<int:pk>/confirm-delete/', views_dir.todoTaskView.ToDoItemDeleteView.as_view(), name="delete"),
    # path('list/', views_dir.ToDoListView.as_view(), name="list"),
    path('done/', views_dir.todoGroupView.ToDoGroupTasksIndexViewDone.as_view(), name="done"),
    path('createGroup/', views_dir.todoGroupView.ToDoGroupCreateView.as_view(), name="createGroup"),
    path('create/', views_dir.todoTaskView.TodoItemCreateView.as_view(), name="create"),
    path('edit/<int:pk>/', views_dir.todoGroupView.ToDoMarkDoneView.as_view(), name="done_task"),
    path('telegram/', views_dir.todoUtilsView.TelegramProfileView.as_view(), name="tg"),
]