from django.test import TestCase
from django.urls import reverse_lazy, reverse
from employee_tree.models import Employee
from django.http import JsonResponse


class HomePageViewTest(TestCase):
    fixtures = ['employees.json']

    @classmethod
    def setUpTestData(cls):
        # Загружаем данные из фикстуры
        cls.employees = Employee.objects.all()

    def test_view_url_exists_at_desired_location(self):
        # Тестируем URL-адрес по ожидаемому пути
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        # Тестируем URL-адрес по имени маршрута
        response = self.client.get(reverse_lazy('home_page'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Тестируем шаблон
        response = self.client.get(reverse_lazy('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page.html')

    def test_view_context_data(self):
        # Тестируем контекст
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Дерево сотрудников')
        self.assertTrue('employees' in response.context)
        self.assertEqual(len(response.context['employees']), 1)

    def test_view_context_data_child(self):
        # Контекст AJAX-запроса
        response = self.client.get(reverse(
            'employee_children', args=[1]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        json_data = response.json()
        self.assertTrue(isinstance(json_data, list))
        self.assertEqual(len(json_data), 8)
