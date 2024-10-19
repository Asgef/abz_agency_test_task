"""
URL configuration for employee_tree project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    HomePageView, EmployeeChildrenView, EmployeeListView,
    LoadMoreEmployeesView, UserLoginView, UserLogoutView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home_page'),
    path(
        'employee-children/<int:employee_id>/',
        EmployeeChildrenView.as_view(), name='employee_children'
    ),
    path('employee-list/', EmployeeListView.as_view(), name='employee_list'),
    path(
        'load-more-employees/', LoadMoreEmployeesView.as_view(),
        name='load_more_employees'
    ),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
