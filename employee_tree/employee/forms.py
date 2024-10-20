from django import forms
from .models import Employee
from dal import autocomplete


class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Имя'}
        ),
    )

    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Фамилия'}
        ),
    )

    position = forms.ChoiceField(
        label='Должность',
        choices=Employee.POSITION_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Должность'}
        ),
    )

    hire_date = forms.DateField(
        label='Дата приема',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}
        ),
    )

    salary = forms.IntegerField(
        label='Зарплата',
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Зарплата'}
        ),
    )

    manager = forms.ModelChoiceField(
        label='Руководитель',
        queryset=Employee.objects.all(),
        widget=autocomplete.ModelSelect2(url='employee-autocomplete'),
        required=False
    )

    class Meta:
        model = Employee
        fields = (
            'first_name', 'last_name', 'position',
            'hire_date','salary', 'manager',
        )