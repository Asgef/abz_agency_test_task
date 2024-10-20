from employee_tree.mixins import AuthRequiredMixin
from employee_tree.employee.models import Employee
from django_filters.views import FilterView
from employee_tree.employee.filters import EmployeeFilter
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from employee_tree.employee.forms import EmployeeForm
from dal import autocomplete
from django.db.models import Q
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)


class EmployeeListView(AuthRequiredMixin, FilterView, ListView):
    """
    Django view class that displays a list of employees.

    This class uses a `FilterView` to filter employees based on
    a `EmployeeFilter` class.
    It paginates the results, showing 20 employees per page.
    The employees are ordered based on a query parameter `ordering`
    (defaults to `id` if not specified).
    The filtered and ordered employees are passed to the `employee_list.html`
    template as a context variable `employees`.

    The class includes an extra context variable `title` with the value
    `'List of employees'`.
    """
    model = Employee
    template_name = 'employee_list.html'
    filterset_class = EmployeeFilter
    context_object_name = 'employees'
    extra_context = {
        'title': 'Список сотрудников'
    }
    paginate_by = 20

    def get_ordering(self):
        """
        Returns the ordering parameter based on the query parameter `ordering`.

        The `ordering` parameter can be one of the following:
        - 'first_name'
        - 'last_name'
        - 'position'
        - 'hire_date'
        - 'salary'
        - 'manager__last_name'
        - '-first_name'
        - '-last_name'
        - '-position'
        - '-hire_date'
        - '-salary'
        - '-manager__last_name'

        If the `ordering` parameter is not in the list above,
        the default ordering is 'id'.
        """
        ordering = self.request.GET.get('ordering')
        if ordering in [
            'first_name', 'last_name', 'position', 'hire_date', 'salary',
            'manager__last_name', '-first_name', '-last_name', '-position',
            '-hire_date', '-salary', '-manager__last_name'
        ]:
            return ordering
        return 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Returns the context data for the view.

        The context data includes the filtered and ordered employees, as well
        as the extra context variable `title`.
        """
        context = super().get_context_data(**kwargs)
        filterset = self.filterset_class(
            self.request.GET, queryset=self.get_queryset()
        )
        filtered_queryset = filterset.qs.order_by(self.get_ordering())
        context['employees'] = filtered_queryset[:self.paginate_by]
        return context


class EmployeeShowView(AuthRequiredMixin, DetailView):
    """
    Django view class that displays detailed information about an employee.

    The detailed information is passed to the `employee_show.html` template as
    a context variable `employee`.
    The class includes an extra context variable `title` with the value
    `'Информация о сотруднике'`.
    """
    model = Employee
    template_name = 'employee_show.html'
    context_object_name = 'employee'
    extra_context = {
        'title': 'Информация о сотруднике'
    }


class EmployeeAddView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Django view class that creates a new employee.

    The form class for creating a new employee is `EmployeeForm`.
    The success URL is set to `reverse_lazy('employee_list')`.
    The success message is set to `'Сотрудник успешно создан'`.
    The class includes an extra context variable `title` with the value
    `'Создание сотрудника'`.
    The extra context variable `button_text` is set to `'Создать'`.
    """
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
    """
    Django view class that edits an existing employee.

    The form class for editing an employee is `EmployeeForm`.
    The success URL is set to `reverse_lazy('employee_list')`.
    The success message is set to `'Сотрудник успешно отредактирован'`.
    The class includes an extra context variable `title` with the value
    `'Редактирование сотрудника'`.
    The extra context variable `button_text` is set to `'Редактировать'`.
    """
    model = Employee
    template_name = 'layouts/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    success_message = 'Сотрудник успешно отредактирован'
    extra_context = {
        'title': 'Редактирование сотрудника',
        'button_text': 'Редактировать',
    }


class EmployeeDeleteView(
    AuthRequiredMixin, SuccessMessageMixin, DeleteView
):
    """
    Django view class that deletes an existing employee.

    The success URL is set to `reverse_lazy('employee_list')`.
    The success message is set to `'Сотрудник успешно удален'`.
    The class includes an extra context variable `title` with the value
    `'Удаление сотрудника'`.
    The extra context variable `button_text` is set to `'Да, удалить'`.
    """
    model = Employee
    template_name = 'layouts/delete.html'
    success_url = reverse_lazy('employee_list')
    success_message = 'Сотрудник успешно удален'
    extra_context = {
        'title': 'Удаление сотрудника',
        'button_text': 'Да, удалить',
    }


class LoadMoreEmployeesView(View):
    """
    Django view class that loads more employees.

    This view is used to load more employees when the user
    scrolls down the page.
    It returns a JSON response with the HTML of the loaded employees.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the GET request.

        Returns a JSON response with the HTML of the loaded employees.
        """
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
    """
    Django view class that provides autocomplete functionality for employees.

    This view is used to provide autocomplete suggestions for employees
    when the user types in the search field.
    """
    def get_queryset(self):
        """
        Returns the queryset of employees.

        The queryset is filtered based on the search term entered by the user.
        """
        # проверка авторизации
        if not self.request.user.is_authenticated:
            return Employee.objects.none()

        queryset = Employee.objects.all()

        if self.q:
            terms = self.q.split()
            # Ищем по каждому слову в `first_name` и `last_name`
            for term in terms:
                queryset = queryset.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term)
                )

        return queryset
