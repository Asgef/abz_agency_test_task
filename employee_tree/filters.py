from django_filters import FilterSet, DateFilter, NumberFilter, ChoiceFilter
from .models import Employee


class EmployeeFilter(FilterSet):
    hire_date_start = DateFilter(field_name='hire_date', lookup_expr='gte')
    hire_date_end = DateFilter(field_name='hire_date', lookup_expr='lte')
    salary_min = NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = NumberFilter(field_name='salary', lookup_expr='lte')
    position = ChoiceFilter(choices=Employee.POSITION_CHOICES)

    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'position',
            'hire_date_start',
            'hire_date_end',
            'salary_min',
            'salary_max'
        ]
