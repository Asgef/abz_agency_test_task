from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):
    """
    A mixin class that requires authentication for a view.

    If the user is not authenticated, it redirects them to the login
    page and displays an error message.
    """

    auth_message = 'Вы не авторизованы. Пожалуйста, войдите в систему.'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        """
        Handles the dispatch of the view.

        If the user is not authenticated, it redirects them to the login page
        and displays an error message.
        Otherwise, it calls the parent class's dispatch method.

        :param request: The request object
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        :return: A redirect to the login page or the result of the parent
        class's dispatch method
        """
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
