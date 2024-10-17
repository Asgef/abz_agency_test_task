from django.views.generic import ListView
from employee_tree.models import Employee
from .filters import EmployeeFilter
from django_filters.views import FilterView
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.shortcuts import render


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

        if object_list is None:
            object_list = self.filter_queryset(self.get_queryset())

        paginator = Paginator(object_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            employees = paginator.page(page)
        except PageNotAnInteger:
            employees = paginator.page(1)
        except EmptyPage:
            employees = paginator.page(paginator.num_pages)

        context['employees'] = employees
        return context


