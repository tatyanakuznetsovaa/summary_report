import csv

PROMPT = """
1. Вывести в понятном виде иерархию команд, т.е. департамент и все команды,
которые входят в него
2. Вывести сводный отчёт по департаментам: название, численность,
"вилка" зарплат в виде мин – макс, среднюю зарплату
3. Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.
"""


def read_data() -> list[dict]:
    """
    Считывает данные из csv файла Corp_Summary и возвращает в формате списка
    """
    with open("data\Corp_Summary.csv", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        return list(reader)


def print_commands_hierachy():
    """
    Выводит в понятном виде иерархию команд, т.е. департамент и все команды,
    которые входят в него
    """
    data = read_data()
    teams_by_departments = dict()
    for row in data:
        department = row["Департамент"]
        team = row["Отдел"]
        teams = teams_by_departments.setdefault(department, set())
        teams.add(team)
    for department, teams in teams_by_departments.items():
        print(department)
        for team in teams:
            print(" " * 3, team)


def get_salary_summary(data: list[dict]) -> dict[str, dict[str, object]]:
    salaries_of_department = dict()
    for row in data:
        department = row["Департамент"]
        salaries = salaries_of_department.setdefault(department, [])
        salary = float(row["Оклад"])
        salaries.append(salary)
    summary = dict()
    for department, salaries in salaries_of_department.items():
        summary[department] = {
            "Численность": len(salaries),
            "Минимальная зарплата": min(salaries),
            "Максимальная зарплата": max(salaries),
            "Средняя зарплата": sum(salaries) / len(salaries),
        }
    return summary


def print_corp_summary():
    """Выводит сводный отчет по департаментам: название, численность,
    "вилка" зарплат в виде мин – макс, среднюю зарплату"""
    data = read_data()
    summary = get_salary_summary(data)
    for department, statistics in summary.items():
        print(f"Департамент: {department}")
        for statistic, value in statistics.items():
            print(f"   {statistic}: {value}")


def save_corp_summary():
    """Сохраняет сводный отчёт из предыдущего пункта в виде csv-файла."""
    data = read_data()
    summary = get_salary_summary(data)
    columns = [
        "Департамент",
        "Численность",
        "Минимальная зарплата",
        "Максимальная зарплата",
        "Средняя зарплата",
    ]
    text = ";".join(columns)
    text += "\n"
    for department, statistics in summary.items():
        text += department
        text += ";"
        text += str(statistics["Численность"])
        text += ";"
        text += str(statistics["Минимальная зарплата"])
        text += ";"
        text += str(statistics["Максимальная зарплата"])
        text += ";"
        text += str(statistics["Средняя зарплата"])
        text += "\n"
    with open("data\output.csv", "wb") as csv_file:
        csv_file.write(text.encode("utf-8"))
    print("Данные успешно сохранены")


if __name__ == "__main__":
    print(PROMPT)
    while True:
        choice = input()
        if choice == "1":
            print_commands_hierachy()
        elif choice == "2":
            print_corp_summary()
        elif choice == "3":
            save_corp_summary()
        else:
            print(f'Опция "{choice}" не поддерживается')
