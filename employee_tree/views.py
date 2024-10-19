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
    model = Employee
    template_name = 'home_page.html'
    context_object_name = 'employees'
    extra_context = {
        'title': 'Дерево сотрудников'
    }

    def get_queryset(self):
        # Загрузить первый уровень иерархии
        return Employee.objects.filter(manager_id=None)


class EmployeeChildrenView(View):
    def get(self, request, employee_id):
        # Загрузить подчинённых для данного сотрудника
        children = Employee.objects.filter(
            manager_id=employee_id).values(
            'id', 'first_name', 'last_name', 'position', 'manager_id'
            )
        return JsonResponse(list(children), safe=False)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'layouts/form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home_page')
    success_message = 'Вы вошли в систему'
    extra_context = {
        'title': 'Вход',
        'button_text': 'Вход',
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли из системы')
        return super().dispatch(request, *args, **kwargs)
