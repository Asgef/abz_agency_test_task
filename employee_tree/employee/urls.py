from django.urls import path
from .views import EmployeeListView, LoadMoreEmployeesView


urlpatterns = [
        path('', EmployeeListView.as_view(), name='employee_list'),
        path(
            'load-more-employees/', LoadMoreEmployeesView.as_view(),
            name='load_more_employees'
        ),
]
