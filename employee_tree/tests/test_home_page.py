from django.test import TestCase
from django.urls import reverse_lazy, reverse
from employee_tree.models import Employee


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
        self.assertEqual(len(response.context['employees']), 50)

    # def test_view_displays_employees(self):
    #     # Тестируем, отображение сотрудников
    #     response = self.client.get('/')
    #     for employee in self.employees:
    #         self.assertContains(response, employee.name)
    #         self.assertContains(response, employee.position)
