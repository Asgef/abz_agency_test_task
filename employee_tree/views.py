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
            'id', 'name', 'position', 'manager_id'
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
        if ordering in [
            'first_name', 'last_name', 'position', 'hire_date', 'salary',
            'manager__last_name', '-first_name', '-last_name', '-position',
            '-hire_date', '-salary', '-manager__last_name'
        ]:
            return ordering
        return 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = self.filterset_class(
            self.request.GET, queryset=self.get_queryset()
        )
        filtered_queryset = filterset.qs.order_by(self.get_ordering())
        context['employees'] = filtered_queryset[:self.paginate_by]
        return context


class LoadMoreEmployeesView(View):
    def get(self, request, *args, **kwargs):
        offset = int(request.GET.get('offset', 0))
        limit = 20
        ordering = request.GET.get('ordering', 'id')

        employees = Employee.objects.all().order_by(ordering)[
                    offset:offset + limit
                    ]
        html = render_to_string(
            'employee_rows.html', {'employees': employees}
        )
        return JsonResponse({'html': html})
