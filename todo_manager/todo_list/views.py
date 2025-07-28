from datetime import timedelta

from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ToDoItemCreateForm, ToDoItemUpdateForm, GroupCreateForm
from .mixins import UserQuerySetMixin, UserObjectPermissionMixin, UserFormKwargsMixin
from .models import ToDoItem, ToDoGroup


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .tasks import send_task_reminder


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'todo_list/registration/register.html'
    success_url = reverse_lazy('login')  # после успешной регистрации


class ToDoDetailView(LoginRequiredMixin, UserObjectPermissionMixin, DetailView):
    model = ToDoItem
    queryset = ToDoItem.objects.filter(archived=False)

class TodoItemCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = ToDoItem
    form_class = ToDoItemCreateForm
    success_url = reverse_lazy('todo_list:index')

    def form_valid(self, form):
        # Привязываем задачу к текущему пользователю
        form.instance.owner = self.request.user
        # Если группа не выбрана, устанавливаем фиктивную группу "Без группы"
        if not form.instance.group:
            try:
                default_group = ToDoGroup.objects.get(name="Без группы", owner=self.request.user)
            except ToDoGroup.DoesNotExist:
                raise ValueError("Не найдена группа 'Без группы' для пользователя!")

            form.instance.group = default_group
        response = super().form_valid(form)

        task = form.instance
        notify_time = task.execute_time - timedelta(minutes=task.remind_before)

        if notify_time > now():
            send_task_reminder.apply_async(
                args=[task.id],
                eta=notify_time
            )
        else:
            print("Время напоминания уже прошло — задача не ставится.")

        return response


class ToDoItemUpdateView(LoginRequiredMixin, UserFormKwargsMixin, UserObjectPermissionMixin, UpdateView):
    template_name_suffix = "_update_form"
    model = ToDoItem
    form_class = ToDoItemUpdateForm


class ToDoItemDeleteView(LoginRequiredMixin, UserObjectPermissionMixin, DeleteView):
    model = ToDoItem
    success_url = reverse_lazy("todo_list:index")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ToDoGroupCreateView(LoginRequiredMixin, CreateView):
    model = ToDoGroup
    form_class = GroupCreateForm
    template_name = "todo_list/todogroup_form.html"
    success_url = reverse_lazy('todo_list:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # присваиваем owner
        return super().form_valid(form)


class BaseGroupTasksView(TemplateView):
    template_name = 'todo_list/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        groups = ToDoGroup.objects.filter(owner=user).prefetch_related('tasks')

        data = []
        for group in groups:
            tasks = group.tasks.filter(**self.task_filter)
            data.append({
                "group": group.name,
                "tasks": tasks,
            })

        context["data"] = data

        return context


class ToDoGroupWithTasksIndexView(LoginRequiredMixin, BaseGroupTasksView):
    task_filter = {"archived": False}


class ToDoGroupTasksIndexViewDone(LoginRequiredMixin, BaseGroupTasksView):
    task_filter = {"archived": False, "done": True}


class ToDoMarkDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(ToDoItem, pk=pk, owner=request.user)
        task.done = True
        task.save()
        return redirect('todo_list:index')