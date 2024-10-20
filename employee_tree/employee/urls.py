from django.urls import path
from .views import (
    EmployeeListView, LoadMoreEmployeesView, EmployeeShowView,
    EmployeeAddView, EmployeeAutocomplete
)


urlpatterns = [
        path('', EmployeeListView.as_view(), name='employee_list'),
        path(
            'load-more-employees/', LoadMoreEmployeesView.as_view(),
            name='load_more_employees'
        ),
        path(
            'employee-autocomplete/', EmployeeAutocomplete.as_view(),
            name='employee-autocomplete'
        ),
        path('create/', EmployeeAddView.as_view(), name='employee_add'),
        path('<int:pk>/', EmployeeShowView.as_view(), name='employee_show'),
        # path('<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
        # path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
]
