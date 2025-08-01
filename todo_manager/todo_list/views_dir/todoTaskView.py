from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from todo_list.forms import ToDoItemCreateForm, ToDoItemUpdateForm
from todo_list.mixins import UserObjectPermissionMixin, UserFormKwargsMixin
from todo_list.models import ToDoItem, ToDoGroup
from todo_list.tasks import send_task_reminder


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


