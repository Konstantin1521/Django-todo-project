from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from  . models import ToDoItem

class ToDoListIndexView(ListView):
    template_name = "todo_list/index.html"
    queryset = ToDoItem.objects.all()[:3]


class ToDoListView(ListView):
    # template_name = "todo_list/index.html"
    model = ToDoItem

class ToDoListDoneView(ListView):
    queryset = ToDoItem.objects.filter(done=True).all()


class ToDoDetailView(DetailView):
    model = ToDoItem

# Create your views here.
# def index_view(request: HttpRequest) -> HttpResponse:
#     todo_items = ToDoItem.objects.all()
#     return  render(
#         request,
#         template_name="todo_list/index.html",
#         context={"todo_items": todo_items[:3]}
#     )