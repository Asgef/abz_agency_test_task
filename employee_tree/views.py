from django.views.generic import ListView
from employee_tree.models import Employee
from .filters import EmployeeFilter
from django_filters.views import FilterView
from django.http import JsonResponse
from django.views import View


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


class EmployeeListView(FilterView, ListView):
    model = Employee
    template_name = 'employee_list.html'
    filterset_class = EmployeeFilter
    context_object_name = 'employees'
    extra_context = {
        'title': 'Список сотрудников'
    }
    paginate_by = 20
    ordering = 'id'
