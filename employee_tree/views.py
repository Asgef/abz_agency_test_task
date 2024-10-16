from django.views.generic import ListView
from employee_tree.models import Employee
from .filters import EmployeeFilter
from django_filters.views import FilterView
from django.http import JsonResponse
from django.views import View
from django.template.loader import render_to_string


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

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering in ['first_name', 'last_name', 'position', 'hire_date', 'salary', 'manager', '-first_name', '-last_name', '-position', '-hire_date', '-salary', '-manager']:
            return ordering
        return 'id'

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            html = render_to_string('employee_list.html', context, request=request)
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)
