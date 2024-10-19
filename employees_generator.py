from django_seed import Seed
from django.db import transaction
import random
import django
import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'employee_tree.settings'
)
django.setup()

from employee_tree.models import Employee  # noqa E402


seeder = Seed.seeder()

positions = [
    "Генеральный директор", "Руководитель отдела",
    "Менеджер", "Старший инженер", "Инженер"
]
def main():
    if Employee.objects.get(id=1):
        print("Employees already exists")
        return

    # Создать первого сотрудника "Генеральный директор"
    print("Creating employees...")
    if not Employee.objects.filter(id=1).exists():
        gen_dir = Employee.objects.create(
            id=1,
            first_name=seeder.faker.first_name(),
            last_name=seeder.faker.last_name(),
            position="Генеральный директор",
            hire_date=seeder.faker.date_this_century(),
            salary=random.randint(300000, 500000),
            manager=None
        )

    # Создать других сотрудников
    with transaction.atomic():
        # Создать уровень "Руководитель отдела"
        heads = []
        for i in range(2, 12):
            head = Employee.objects.create(
                id=i,
                first_name=seeder.faker.first_name(),
                last_name=seeder.faker.last_name(),
                position="Руководитель отдела",
                hire_date=seeder.faker.date_this_century(),
                salary=random.randint(200000, 300000),
                manager=gen_dir
            )
            heads.append(head)

        # Создать уровень "Менеджер"
        managers = []
        for i in range(12, 102):
            manager = Employee.objects.create(
                id=i,
                first_name=seeder.faker.first_name(),
                last_name=seeder.faker.last_name(),
                position="Менеджер",
                hire_date=seeder.faker.date_this_century(),
                salary=random.randint(150000, 200000),
                manager=random.choice(heads)
            )
            managers.append(manager)

        # Создать уровень "Старший инженер"
        senior_engineers = []
        for i in range(102, 1002):
            senior_engineer = Employee.objects.create(
                id=i,
                first_name=seeder.faker.first_name(),
                last_name=seeder.faker.last_name(),
                position="Старший инженер",
                hire_date=seeder.faker.date_this_century(),
                salary=random.randint(100000, 150000),
                manager=random.choice(managers)
            )
            senior_engineers.append(senior_engineer)

        # Создать уровень "Инженер"
        for i in range(1002, 50001):
            Employee.objects.create(
                id=i,
                first_name=seeder.faker.first_name(),
                last_name=seeder.faker.last_name(),
                position="Инженер",
                hire_date=seeder.faker.date_this_century(),
                salary=random.randint(50000, 100000),
                manager=random.choice(senior_engineers)
            )

    print(f"Created {Employee.objects.count()} employees.")


if __name__ == "__main__":
    main()

