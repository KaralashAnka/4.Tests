#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для работы с данными сотрудников (адаптированный для тестирования)
"""

from datetime import datetime
from typing import Dict, List, Optional, Union

# Имитируем базу данных сотрудников
_employees_db = [
    {"id": 1, "name": "Иванов И.И.", "position": "Менеджер", "salary": 120000.0, "hire_date": "2023-01-15"},
    {"id": 2, "name": "Петров П.П.", "position": "Программист", "salary": 180000.0, "hire_date": "2023-02-20"},
    {"id": 3, "name": "Сидоров С.С.", "position": "Аналитик", "salary": 150000.0, "hire_date": "2023-03-10"}
]

_next_employee_id = 4


def get_employees() -> List[Dict]:
    """
    Функция для получения списка сотрудников

    Returns:
        list: Список всех сотрудников
    """
    print("👥 Загружаем список сотрудников из базы данных...")
    print("   - Подключение к базе данных")
    print("   - Выборка активных сотрудников")
    print("   - Проверка актуальности данных")

    print(f"✅ Загружено {len(_employees_db)} сотрудников")
    print(f"   Время загрузки: {datetime.now().strftime('%H:%M:%S')}")

    return _employees_db.copy()


def get_employee_by_id(employee_id: int) -> Optional[Dict]:
    """
    Получить сотрудника по ID

    Args:
        employee_id: ID сотрудника

    Returns:
        dict или None: Данные сотрудника или None если не найден
    """
    if not isinstance(employee_id, int):
        raise TypeError("ID сотрудника должен быть целым числом")

    for employee in _employees_db:
        if employee['id'] == employee_id:
            print(f"🔍 Найден сотрудник: {employee['name']}")
            return employee.copy()

    print(f"❌ Сотрудник с ID {employee_id} не найден")
    return None


def add_employee(name: str, position: str, salary: float = 100000.0) -> Dict:
    """
    Добавить нового сотрудника

    Args:
        name: Имя сотрудника
        position: Должность
        salary: Зарплата (по умолчанию 100000)

    Returns:
        dict: Данные добавленного сотрудника

    Raises:
        ValueError: При некорректных данных
    """
    global _next_employee_id

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Имя сотрудника должно быть непустой строкой")

    if not isinstance(position, str) or not position.strip():
        raise ValueError("Должность должна быть непустой строкой")

    if not isinstance(salary, (int, float)) or salary <= 0:
        raise ValueError("Зарплата должна быть положительным числом")

    new_employee = {
        'id': _next_employee_id,
        'name': name.strip(),
        'position': position.strip(),
        'salary': float(salary),
        'hire_date': datetime.now().strftime('%Y-%m-%d')
    }

    _employees_db.append(new_employee)
    _next_employee_id += 1

    print(f"➕ Добавлен новый сотрудник: {name} - {position}")
    return new_employee.copy()


def remove_employee(employee_id: int) -> bool:
    """
    Удалить сотрудника по ID

    Args:
        employee_id: ID сотрудника для удаления

    Returns:
        bool: True если сотрудник удален, False если не найден

    Raises:
        TypeError: При некорректном типе ID
    """
    if not isinstance(employee_id, int):
        raise TypeError("ID сотрудника должен быть целым числом")

    for i, employee in enumerate(_employees_db):
        if employee['id'] == employee_id:
            removed_employee = _employees_db.pop(i)
            print(f"🗑️ Удален сотрудник: {removed_employee['name']}")
            return True

    print(f"❌ Сотрудник с ID {employee_id} не найден для удаления")
    return False


def update_employee_data(employee_id: int, **kwargs) -> Optional[Dict]:
    """
    Обновить данные сотрудника

    Args:
        employee_id: ID сотрудника
        **kwargs: Поля для обновления

    Returns:
        dict или None: Обновленные данные сотрудника или None если не найден
    """
    if not isinstance(employee_id, int):
        raise TypeError("ID сотрудника должен быть целым числом")

    for employee in _employees_db:
        if employee['id'] == employee_id:
            # Обновляем только разрешенные поля
            allowed_fields = ['name', 'position', 'salary']
            updated_fields = []

            for field, value in kwargs.items():
                if field in allowed_fields:
                    if field == 'name' and (not isinstance(value, str) or not value.strip()):
                        raise ValueError("Имя должно быть непустой строкой")
                    if field == 'position' and (not isinstance(value, str) or not value.strip()):
                        raise ValueError("Должность должна быть непустой строкой")
                    if field == 'salary' and (not isinstance(value, (int, float)) or value <= 0):
                        raise ValueError("Зарплата должна быть положительным числом")

                    employee[field] = value
                    updated_fields.append(field)

            if updated_fields:
                print(f"🔄 Обновлены поля {updated_fields} для сотрудника {employee['name']}")
                return employee.copy()
            else:
                print("❌ Нет полей для обновления")
                return employee.copy()

    print(f"❌ Сотрудник с ID {employee_id} не найден")
    return None


def get_employees_by_position(position: str) -> List[Dict]:
    """
    Получить сотрудников по должности

    Args:
        position: Должность для поиска

    Returns:
        list: Список сотрудников с указанной должностью
    """
    if not isinstance(position, str):
        raise TypeError("Должность должна быть строкой")

    filtered_employees = [
        emp.copy() for emp in _employees_db
        if emp['position'].lower() == position.lower()
    ]

    print(f"🎯 Найдено {len(filtered_employees)} сотрудников с должностью '{position}'")
    return filtered_employees


def get_employees_count() -> int:
    """
    Получить количество сотрудников

    Returns:
        int: Количество сотрудников в базе
    """
    return len(_employees_db)


def clear_employees_db() -> None:
    """
    Очистить базу данных сотрудников (для тестирования)
    """
    global _employees_db, _next_employee_id
    _employees_db.clear()
    _next_employee_id = 1
    print("🧹 База данных сотрудников очищена")


def reset_employees_db() -> None:
    """
    Сбросить базу данных к начальному состоянию (для тестирования)
    """
    global _employees_db, _next_employee_id
    _employees_db = [
        {"id": 1, "name": "Иванов И.И.", "position": "Менеджер", "salary": 120000.0, "hire_date": "2023-01-15"},
        {"id": 2, "name": "Петров П.П.", "position": "Программист", "salary": 180000.0, "hire_date": "2023-02-20"},
        {"id": 3, "name": "Сидоров С.С.", "position": "Аналитик", "salary": 150000.0, "hire_date": "2023-03-10"}
    ]
    _next_employee_id = 4
    print("🔄 База данных сотрудников сброшена к начальному состоянию")