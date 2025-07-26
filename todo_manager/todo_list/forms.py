from django import forms

from todo_list.models import ToDoItem, ToDoGroup


class ToDoItemCreateForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ("title", "description", "group")

    group = forms.ModelChoiceField(
        queryset=ToDoGroup.objects.none(),  # пустой queryset по умолчанию
        required=False  # делаем поле необязательным
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор групп только теми, что принадлежат пользователю
        if user:
            self.fields['group'].queryset = ToDoGroup.objects.filter(owner=user)


class ToDoItemUpdateForm(forms.ModelForm):
    class Meta(ToDoItemCreateForm.Meta):
        fields = ("title", "description", "done", "group",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор групп только теми, что принадлежат пользователю
        if user:
            self.fields['group'].queryset = ToDoGroup.objects.filter(owner=user)


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = ToDoGroup
        fields = ("name",)
