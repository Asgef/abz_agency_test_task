from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):

    auth_message = 'Вы не авторизованы. Пожалуйста, войдите в систему.'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
