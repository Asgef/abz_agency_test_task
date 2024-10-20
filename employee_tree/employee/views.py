from employee_tree.mixins import AuthRequiredMixin
from employee_tree.employee.models import Employee
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from employee_tree.employee.filters import EmployeeFilter
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from employee_tree.employee.forms import EmployeeForm
from dal import autocomplete
from django.db.models import Q


class EmployeeListView(AuthRequiredMixin, FilterView, ListView):
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



class EmployeeShowView(AuthRequiredMixin, DetailView):
    model = Employee
    template_name = 'employee_show.html'
    context_object_name = 'employee'
    extra_context = {
        'title': 'Информация о сотруднике'
    }


class EmployeeAddView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employee
    template_name = 'layouts/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    success_message = 'Сотрудник успешно создан'
    extra_context = {
        'title': 'Создание сотрудника',
        'button_text': 'Создать',
    }


class EmployeeEditView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'layouts/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    success_message = 'Сотрудник успешно отредактирован'
    extra_context = {
        'title': 'Редактирование сотрудника',
        'button_text': 'Редактировать',
    }


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


class EmployeeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # проверка авторизации
        if not self.request.user.is_authenticated:
            return Employee.objects.none()

        queryset = Employee.objects.all()

        if self.q:
            terms = self.q.split()
            # Ищем по каждому слову в `first_name` и `last_name`
            for term in terms:
                queryset = queryset.filter(
                    Q(first_name__icontains=term) | Q(last_name__icontains=term)
                )

        return queryset
