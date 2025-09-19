#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для расчета зарплаты сотрудников (адаптированный для тестирования)
"""

from datetime import datetime
from typing import Dict, List, Optional, Union


def calculate_salary(employees: Optional[List[Dict]] = None) -> Dict:
    """
    Функция для расчета зарплаты сотрудников

    Args:
        employees: Список сотрудников для расчета

    Returns:
        dict: Результат расчета зарплаты
    """
    if employees is None:
        from application.db.people import get_employees
        employees = get_employees()

    calculation_date = datetime.now().strftime('%d.%m.%Y')

    # Имитируем расчет зарплаты
    total_salary = 0
    salary_details = []

    for employee in employees:
        base_salary = employee.get('salary', 100000)  # Базовая зарплата
        bonus = base_salary * 0.1  # 10% премия
        total = base_salary + bonus

        salary_details.append({
            'employee_id': employee['id'],
            'name': employee['name'],
            'base_salary': base_salary,
            'bonus': bonus,
            'total': total
        })

        total_salary += total

    result = {
        'calculation_date': calculation_date,
        'total_employees': len(employees),
        'salary_details': salary_details,
        'total_salary': total_salary,
        'average_salary': total_salary / len(employees) if employees else 0,
        'status': 'calculated'
    }

    print("🧮 Выполняется расчет зарплаты...")
    print("   - Обработка базовых окладов")
    print("   - Расчет премий и надбавок")
    print("   - Вычисление налогов и удержаний")
    print(f"   - Дата расчета: {calculation_date}")
    print("✅ Расчет зарплаты завершен!")

    return result


def calculate_individual_salary(base_salary: float, bonus_percent: float = 0.0) -> Dict:
    """
    Расчет зарплаты для конкретного сотрудника

    Args:
        base_salary: Базовая зарплата
        bonus_percent: Процент премии

    Returns:
        dict: Детали расчета зарплаты
    """
    if not isinstance(base_salary, (int, float)) or base_salary <= 0:
        raise ValueError("Базовая зарплата должна быть положительным числом")

    if not isinstance(bonus_percent, (int, float)) or bonus_percent < 0:
        raise ValueError("Процент премии должен быть неотрицательным числом")

    bonus = base_salary * (bonus_percent / 100)
    total = base_salary + bonus

    return {
        'base_salary': base_salary,
        'bonus_percent': bonus_percent,
        'bonus_amount': bonus,
        'total_salary': total
    }


def calculate_taxes(gross_salary: float) -> Dict:
    """
    Расчет налогов с зарплаты

    Args:
        gross_salary: Валовая зарплата

    Returns:
        dict: Детали налогообложения
    """
    if not isinstance(gross_salary, (int, float)) or gross_salary < 0:
        raise ValueError("Зарплата должна быть неотрицательным числом")

    income_tax_rate = 0.13  # 13% подоходный налог
    social_tax_rate = 0.22  # 22% социальные взносы

    income_tax = gross_salary * income_tax_rate
    social_tax = gross_salary * social_tax_rate
    net_salary = gross_salary - income_tax
    total_taxes = income_tax + social_tax

    return {
        'gross_salary': gross_salary,
        'income_tax': income_tax,
        'social_tax': social_tax,
        'net_salary': net_salary,
        'total_taxes': total_taxes,
        'tax_rate': income_tax_rate
    }


def get_salary_report(format_type: str = 'summary') -> Dict:
    """
    Функция для генерации отчета по зарплате

    Args:
        format_type: Тип отчета ('summary', 'detailed', 'csv')

    Returns:
        dict: Данные отчета
    """
    valid_formats = ['summary', 'detailed', 'csv']
    if format_type not in valid_formats:
        raise ValueError(f"Неподдерживаемый формат отчета. Доступны: {valid_formats}")

    report_data = {
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'format': format_type,
        'status': 'generated',
        'report_id': f"SAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }

    if format_type == 'detailed':
        report_data['includes'] = ['employee_details', 'tax_breakdown', 'bonus_calculation']
    elif format_type == 'summary':
        report_data['includes'] = ['total_amount', 'employee_count']

    print("📊 Отчет по зарплате сгенерирован")
    return report_data


def validate_salary_data(salary_data: Dict) -> tuple:
    """
    Валидация данных зарплаты

    Args:
        salary_data: Данные для валидации

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not isinstance(salary_data, dict):
        return False, "Данные должны быть словарем"

    required_fields = ['base_salary', 'total_salary']
    for field in required_fields:
        if field not in salary_data:
            return False, f"Отсутствует обязательное поле: {field}"

    if salary_data['base_salary'] <= 0:
        return False, "Базовая зарплата должна быть положительной"

    if salary_data['total_salary'] < salary_data['base_salary']:
        return False, "Общая зарплата не может быть меньше базовой"

    return True, "Данные корректны"