from django.views.generic import ListView
from employee_tree.employee.models import Employee
from django.views import View
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy


class HomePageView(ListView):
    """
    The presentation class for the home page.

    Displays the employee tree on the main page.
    """
    model = Employee
    template_name = 'home_page.html'
    context_object_name = 'employees'
    extra_context = {
        'title': 'Дерево сотрудников'
    }

    def get_queryset(self):
        """
        Returns the top-level employees.

        Loads employees with no manager (manager_id=None).
        """
        # Загрузить первый уровень иерархии
        return Employee.objects.filter(manager_id=None)


class EmployeeChildrenView(View):
    """
    View class for loading employee's subordinates.

    Returns a list of employee's subordinates in JSON format.
    """
    def get(self, request, employee_id):
        """
        Handles a GET request to load an employee's children.

        :param request: The request object
        :param employee_id: The ID of the employee
        :return: A list of the employee's children in JSON format
        """
        # Загрузить подчинённых для данного сотрудника
        children = Employee.objects.filter(
            manager_id=employee_id).values(
            'id', 'first_name', 'last_name', 'position', 'manager_id'
            )
        return JsonResponse(list(children), safe=False)


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    A view class for user login.

    Handles user login and displays a success message.
    """
    template_name = 'layouts/form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home_page')
    success_message = 'Вы вошли в систему'
    extra_context = {
        'title': 'Вход',
        'button_text': 'Вход',
    }


class UserLogoutView(LogoutView):
    """
    A view class for user logout.

    Handles user logout and displays a success message.
    """
    next_page = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из системы')
        return super().dispatch(request, *args, **kwargs)
