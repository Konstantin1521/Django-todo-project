from django.views.generic import (
    CreateView,
)

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'todo_list/registration/register.html'
    success_url = reverse_lazy('login')  # после успешной регистрации