
from django.urls import path
from django.views.generic import TemplateView
from  . import views

app_name = "todo_list"

urlpatterns = [
    path('', views.ToDoListIndexView.as_view(), name="index"),
    path('<int:pk>/', views.ToDoDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', views.ToDoItemUpdateView.as_view(), name="update"),
    path('<int:pk>/confirm-delete/', views.ToDoItemDeleteView.as_view(), name="delete"),
    path('list/', views.ToDoListView.as_view(), name="list"),
    path('done/', views.ToDoListDoneView.as_view(), name="done"),
    path('create/', views.TodoItemCreateView.as_view(), name="create"),
]