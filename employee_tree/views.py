from django.views.generic import ListView
from employee_tree.models import Employee
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
        children = Employee.objects.filter(manager_id=employee_id).values('id', 'name', 'position', 'manager_id')
        return JsonResponse(list(children), safe=False)