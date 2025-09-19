#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Основной модуль программы "Бухгалтерия" (адаптированный для тестирования)
"""

from datetime import datetime
from application.salary import calculate_salary, get_salary_report
from application.db.people import get_employees, update_employee_data


def main():
    """Основная функция программы"""
    result = {
        'status': 'started',
        'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'operations': []
    }

    print("=== Программа 'Бухгалтерия' ===")
    print(f"Дата запуска: {result['start_time']}")
    print()

    # Получаем список сотрудников
    print("Получаем список сотрудников...")
    employees = get_employees()
    result['operations'].append({
        'operation': 'get_employees',
        'result': employees,
        'status': 'success'
    })
    print()

    # Рассчитываем зарплату
    print("Рассчитываем зарплату...")
    salary_data = calculate_salary()
    result['operations'].append({
        'operation': 'calculate_salary',
        'result': salary_data,
        'status': 'success'
    })
    print()

    result['status'] = 'completed'
    result['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("Программа завершена успешно!")
    return result


def get_program_info():
    """Получить информацию о программе"""
    return {
        'name': 'Бухгалтерия',
        'version': '1.0.0',
        'description': 'Программа для ведения бухгалтерской отчетности',
        'modules': ['salary', 'people'],
        'author': 'Student'
    }


def validate_employee_data(employee):
    """Валидация данных сотрудника"""
    if not isinstance(employee, dict):
        return False, "Данные сотрудника должны быть словарем"

    required_fields = ['id', 'name', 'position']
    for field in required_fields:
        if field not in employee:
            return False, f"Отсутствует обязательное поле: {field}"

    if not isinstance(employee['id'], int) or employee['id'] <= 0:
        return False, "ID должен быть положительным числом"

    if not isinstance(employee['name'], str) or not employee['name'].strip():
        return False, "Имя должно быть непустой строкой"

    if not isinstance(employee['position'], str) or not employee['position'].strip():
        return False, "Должность должна быть непустой строкой"

    return True, "Данные корректны"


if __name__ == '__main__':
    main()