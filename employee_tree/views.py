from django.views.generic import ListView
from employee_tree.models import Employee


class HomePageView(ListView):
    model = Employee
    template_name = 'home_page.html'
    context_object_name = 'employees'
    extra_context = {
        'title': 'Дерево сотрудников'
    }
