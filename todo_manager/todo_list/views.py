from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    # TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ToDoItemCreateForm, ToDoItemUpdateForm
from  . models import ToDoItem

class ToDoListIndexView(ListView):
    template_name = "todo_list/index.html"
    queryset = ToDoItem.objects.filter(archived=False).all()[:3]


class ToDoListView(ListView):
    template_name = "todo_list/index.html"
    model = ToDoItem
    queryset = ToDoItem.objects.filter(archived=False)

class ToDoListDoneView(ListView):
    queryset = ToDoItem.objects.filter(done=True, archived=False).all()


class ToDoDetailView(DetailView):
    # model = ToDoItem
    queryset = ToDoItem.objects.filter(archived=False)

class TodoItemCreateView(CreateView):
    model = ToDoItem
    form_class = ToDoItemCreateForm
    # fields = ("title", "description",)


class ToDoItemUpdateView(UpdateView):
    template_name_suffix = "_update_form"
    model = ToDoItem
    form_class = ToDoItemUpdateForm


class ToDoItemDeleteView(DeleteView):
    model = ToDoItem
    success_url = reverse_lazy("todo_list:list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)