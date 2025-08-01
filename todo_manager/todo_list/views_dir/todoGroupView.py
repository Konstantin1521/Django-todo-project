from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from todo_list.forms import GroupCreateForm
from todo_list.models import ToDoGroup, ToDoItem


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


class ToDoGroupTasksIndexViewDone(LoginRequiredMixin, BaseGroupTasksView):
    task_filter = {"archived": False, "done": True}


class ToDoGroupWithTasksIndexView(LoginRequiredMixin, BaseGroupTasksView):
    task_filter = {"archived": False}


class ToDoMarkDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(ToDoItem, pk=pk, owner=request.user)
        task.done = True
        task.save()
        return redirect('todo_list:index')


class ToDoGroupCreateView(LoginRequiredMixin, CreateView):
    model = ToDoGroup
    form_class = GroupCreateForm
    template_name = "todo_list/todogroup_form.html"
    success_url = reverse_lazy('todo_list:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # присваиваем owner
        return super().form_valid(form)
