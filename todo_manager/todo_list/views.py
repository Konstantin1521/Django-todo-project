from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
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
from .mixins import UserQuerySetMixin, UserObjectPermissionMixin
from .models import ToDoItem, ToDoGroup


from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'todo_list/registration/register.html'
    success_url = reverse_lazy('todo_list:list')  # после успешной регистрации


class ToDoListIndexView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = ToDoItem
    template_name = "todo_list/index.html"

    def get_queryset(self):
        # Добавим фильтр по archive, а user фильтрация уже в миксине
        qs = super().get_queryset()
        return qs.filter(archived=False).all()[:3]


class ToDoListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    template_name = "todo_list/index.html"
    model = ToDoItem
    def get_queryset(self):
        # Добавим фильтр по archive, а user фильтрация уже в миксине
        qs = super().get_queryset()
        return qs.filter(archived=False)


class ToDoListDoneView(UserQuerySetMixin, ListView):
    queryset = ToDoItem.objects.filter(done=True, archived=False).all()


class ToDoDetailView(LoginRequiredMixin, UserObjectPermissionMixin, DetailView):
    model = ToDoItem
    queryset = ToDoItem.objects.filter(archived=False)

class TodoItemCreateView(LoginRequiredMixin, CreateView):
    model = ToDoItem
    form_class = ToDoItemCreateForm
    success_url = reverse_lazy('todo_list:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаём текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        # Привязываем задачу к текущему пользователю
        form.instance.owner = self.request.user
        # Если группа не выбрана, устанавливаем фиктивную группу "Без группы"
        if not form.instance.group:
            default_group, created = ToDoGroup.objects.get_or_create(
                name="Без группы",
                owner=self.request.user
            )
            form.instance.group = default_group
        return super().form_valid(form)


class ToDoItemUpdateView(LoginRequiredMixin, UserObjectPermissionMixin, UpdateView):
    template_name_suffix = "_update_form"
    model = ToDoItem
    form_class = ToDoItemUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаём текущего пользователя в форму
        return kwargs


class ToDoItemDeleteView(LoginRequiredMixin, UserObjectPermissionMixin, DeleteView):
    model = ToDoItem
    success_url = reverse_lazy("todo_list:list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)