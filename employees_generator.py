from django_seed import Seed
import random
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_tree.settings')
django.setup()

from employee_tree.models import Employee


seeder = Seed.seeder()

positions = [
    "CEO", "Руководитель отдела", "Менеджер", "Старший инженер", "Инженер"
]

# Create the CEO first
if not Employee.objects.filter(id=1).exists():
    ceo = Employee.objects.create(
        id=1,
        name=seeder.faker.name(),
        position="CEO",
        hire_date=seeder.faker.date_this_century(),
        salary=random.randint(300000, 500000),
        manager=None
    )

# Add other employees
seeder.add_entity(Employee, 49999, {
    'id': lambda x: seeder.faker.unique.random_int(min=2, max=50000),
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: random.choices(positions[1:], weights=[1, 2, 5, 10])[0],
    'hire_date': lambda x: seeder.faker.date_this_century(),
    'salary': lambda x: random.randint(50000, 200000),
    'manager': lambda x: Employee.objects.filter(position__in=positions[:-1]).order_by('?').first(),
})

# Execute the seeding
inserted_pks = seeder.execute()