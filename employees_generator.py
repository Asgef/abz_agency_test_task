import json
import random
from datetime import datetime, timedelta


EMPL_MULTIPLIER = 15


# Генерация случайного имени
first_names = [
    "Иван", "Петр", "Алексей", "Мария", "Светлана", "Елена", "Дмитрий",
    "Ольга", "Наталья", "Кирилл", "Анастасия", "Владимир", "Татьяна", "Сергей",
    "Юлия", "Николай", "Андрей", "Екатерина", "Максим", "Людмила", " Улугбек",
    "Джамшут"
]
last_names = [
    "Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Федоров",
    "Васильев", "Новиков", "Морозов", "Волков", "Зайцев", "Соловьев", "Ершов",
    "Титов", "Орлов", "Макаров", "Борисов", "Григорьев", "Медведев", "Жуков",
    "Кудабергенов", "Зарубин"
]
positions = [
    "CEO", "Руководитель отдела", "Менеджер", "Старший инженер", "Инженер"
]


def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def random_position(level):
    if level == 1:
        return positions[0]
    return positions[min(level - 1, len(positions) - 1)]


def random_salary(level):
    base_salary = 50000
    return base_salary + level * random.randint(5000, 15000)


def random_hire_date():
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2023, 1, 1)
    return start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )


def generate_employees():
    employees = []
    id_counter = 1
    # Генерация первого уровня - CEO
    ceo = {
        "id": id_counter,
        "name": random_name(),
        "position": random_position(1),
        "hire_date": random_hire_date().strftime("%Y-%m-%d"),
        "salary": random_salary(1),
        "manager_id": None
    }
    employees.append(ceo)
    id_counter += 1


    # Генерация остальных уровней
    prev_level_ids = [ceo["id"]]
    for level in range(2, 6):
        current_level_ids = []
        for _ in range(len(prev_level_ids) * EMPL_MULTIPLIER):
            employee = {
                "id": id_counter,
                "name": random_name(),
                "position": random_position(level),
                "hire_date": random_hire_date().strftime("%Y-%m-%d"),
                "salary": random_salary(level),
                "manager_id": random.choice(prev_level_ids)
            }
            employees.append(employee)
            current_level_ids.append(id_counter)
            id_counter += 1
        prev_level_ids = current_level_ids

    return employees


def save_to_json(employees, filename="employees.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(employees, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    employees = generate_employees()
    save_to_json(employees)
    print(
        f"Сгенерировано {len(employees)} "
        f"сотрудников и сохранено в employees.json"
    )
