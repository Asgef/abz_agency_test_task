from django import forms
from django_filters import FilterSet, DateFromToRangeFilter, ChoiceFilter
from .models import Employee


class EmployeeFilter(FilterSet):
    hire_date = DateFromToRangeFilter(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    position = ChoiceFilter(choices=Employee.POSITION_CHOICES)

    class Meta:
        model = Employee
        fields = [
            'name', 'position', 'hire_date', 'salary',
        ]
