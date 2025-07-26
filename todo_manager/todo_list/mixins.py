from django.http import Http404


class UserFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаём текущего пользователя в форму
        return kwargs


class UserQuerySetMixin:
    user_field = 'owner'

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.is_authenticated:
            filter_kwargs = {self.user_field: self.request.user}
            return base_qs.filter(**filter_kwargs)
        return base_qs.none()


class UserObjectPermissionMixin:
    user_field = 'owner'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if getattr(obj, self.user_field) != self.request.user:
            raise Http404("Объект не найден или у вас нет доступа")
        return obj