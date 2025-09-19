#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit-тесты для программы "Бухгалтерия"
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main, get_program_info, validate_employee_data
from application.salary import (
    calculate_salary, calculate_individual_salary, calculate_taxes,
    get_salary_report, validate_salary_data
)
from application.db.people import (
    get_employees, get_employee_by_id, add_employee, remove_employee,
    update_employee_data, get_employees_by_position, get_employees_count,
    clear_employees_db, reset_employees_db
)


class TestMainModule(unittest.TestCase):
    """Тесты основного модуля"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        reset_employees_db()

    def test_get_program_info(self):
        """Тест получения информации о программе"""
        info = get_program_info()

        self.assertIsInstance(info, dict)
        self.assertEqual(info['name'], 'Бухгалтерия')
        self.assertEqual(info['version'], '1.0.0')
        self.assertIn('modules', info)
        self.assertIsInstance(info['modules'], list)

    def test_validate_employee_data_valid(self):
        """Тест валидации корректных данных сотрудника"""
        valid_employee = {
            'id': 1,
            'name': 'Иванов И.И.',
            'position': 'Менеджер'
        }

        is_valid, message = validate_employee_data(valid_employee)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Данные корректны")

    def test_validate_employee_data_invalid(self):
        """Тест валидации некорректных данных сотрудника"""
        # Не словарь
        is_valid, message = validate_employee_data("invalid")
        self.assertFalse(is_valid)
        self.assertIn("словарем", message)

        # Отсутствует обязательное поле
        invalid_employee = {'id': 1, 'name': 'Иван'}
        is_valid, message = validate_employee_data(invalid_employee)
        self.assertFalse(is_valid)
        self.assertIn("position", message)

        # Неправильный тип ID
        invalid_employee = {'id': '1', 'name': 'Иван', 'position': 'Менеджер'}
        is_valid, message = validate_employee_data(invalid_employee)
        self.assertFalse(is_valid)
        self.assertIn("положительным числом", message)

    @patch('builtins.print')
    def test_main_function(self, mock_print):
        """Тест основной функции программы"""
        result = main()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'completed')
        self.assertIn('start_time', result)
        self.assertIn('end_time', result)
        self.assertIn('operations', result)
        self.assertEqual(len(result['operations']), 2)


class TestSalaryModule(unittest.TestCase):
    """Тесты модуля зарплат"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        reset_employees_db()

    @patch('builtins.print')
    def test_calculate_salary(self, mock_print):
        """Тест расчета зарплаты"""
        result = calculate_salary()

        self.assertIsInstance(result, dict)
        self.assertIn('total_employees', result)
        self.assertIn('total_salary', result)
        self.assertIn('salary_details', result)
        self.assertEqual(result['total_employees'], 3)
        self.assertGreater(result['total_salary'], 0)

    @patch('builtins.print')
    def test_calculate_salary_with_custom_employees(self, mock_print):
        """Тест расчета зарплаты с пользовательским списком"""
        custom_employees = [
            {'id': 1, 'name': 'Тест', 'position': 'Тестер', 'salary': 50000}
        ]

        result = calculate_salary(custom_employees)

        self.assertEqual(result['total_employees'], 1)
        self.assertEqual(result['salary_details'][0]['base_salary'], 50000)

    def test_calculate_individual_salary(self):
        """Тест расчета индивидуальной зарплаты"""
        result = calculate_individual_salary(100000, 15)

        self.assertEqual(result['base_salary'], 100000)
        self.assertEqual(result['bonus_percent'], 15)
        self.assertEqual(result['bonus_amount'], 15000)
        self.assertEqual(result['total_salary'], 115000)

    def test_calculate_individual_salary_invalid_input(self):
        """Тест расчета зарплаты с некорректными данными"""
        with self.assertRaises(ValueError):
            calculate_individual_salary(-1000, 10)

        with self.assertRaises(ValueError):
            calculate_individual_salary(100000, -5)

    def test_calculate_taxes(self):
        """Тест расчета налогов"""
        result = calculate_taxes(100000)

        self.assertEqual(result['gross_salary'], 100000)
        self.assertEqual(result['income_tax'], 13000)  # 13%
        self.assertEqual(result['social_tax'], 22000)  # 22%
        self.assertEqual(result['net_salary'], 87000)  # 100000 - 13000

    def test_calculate_taxes_invalid_input(self):
        """Тест расчета налогов с некорректными данными"""
        with self.assertRaises(ValueError):
            calculate_taxes(-1000)

    @patch('builtins.print')
    def test_get_salary_report(self, mock_print):
        """Тест генерации отчета по зарплате"""
        result = get_salary_report('summary')

        self.assertIsInstance(result, dict)
        self.assertEqual(result['format'], 'summary')
        self.assertIn('report_date', result)
        self.assertIn('report_id', result)

    def test_get_salary_report_invalid_format(self):
        """Тест генерации отчета с неправильным форматом"""
        with self.assertRaises(ValueError):
            get_salary_report('invalid_format')

    def test_validate_salary_data(self):
        """Тест валидации данных зарплаты"""
        valid_data = {'base_salary': 100000, 'total_salary': 115000}
        is_valid, message = validate_salary_data(valid_data)
        self.assertTrue(is_valid)

        invalid_data = {'base_salary': 100000, 'total_salary': 50000}
        is_valid, message = validate_salary_data(invalid_data)
        self.assertFalse(is_valid)


class TestPeopleModule(unittest.TestCase):
    """Тесты модуля сотрудников"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        reset_employees_db()

    @patch('builtins.print')
    def test_get_employees(self, mock_print):
        """Тест получения списка сотрудников"""
        employees = get_employees()

        self.assertIsInstance(employees, list)
        self.assertEqual(len(employees), 3)
        self.assertIn('id', employees[0])
        self.assertIn('name', employees[0])
        self.assertIn('position', employees[0])

    @patch('builtins.print')
    def test_get_employee_by_id(self, mock_print):
        """Тест получения сотрудника по ID"""
        employee = get_employee_by_id(1)

        self.assertIsNotNone(employee)
        self.assertEqual(employee['id'], 1)
        self.assertEqual(employee['name'], 'Иванов И.И.')

        # Тест с несуществующим ID
        employee = get_employee_by_id(999)
        self.assertIsNone(employee)

    def test_get_employee_by_id_invalid_type(self):
        """Тест получения сотрудника с неправильным типом ID"""
        with self.assertRaises(TypeError):
            get_employee_by_id("invalid")

    @patch('builtins.print')
    def test_add_employee(self, mock_print):
        """Тест добавления нового сотрудника"""
        initial_count = get_employees_count()

        new_employee = add_employee("Новиков Н.Н.", "Дизайнер", 90000)

        self.assertIsInstance(new_employee, dict)
        self.assertEqual(new_employee['name'], "Новиков Н.Н.")
        self.assertEqual(new_employee['position'], "Дизайнер")
        self.assertEqual(new_employee['salary'], 90000)
        self.assertEqual(get_employees_count(), initial_count + 1)

    def test_add_employee_invalid_data(self):
        """Тест добавления сотрудника с некорректными данными"""
        with self.assertRaises(ValueError):
            add_employee("", "Должность")

        with self.assertRaises(ValueError):
            add_employee("Имя", "")

        with self.assertRaises(ValueError):
            add_employee("Имя", "Должность", -1000)

    @patch('builtins.print')
    def test_remove_employee(self, mock_print):
        """Тест удаления сотрудника"""
        initial_count = get_employees_count()

        # Удаляем существующего сотрудника
        result = remove_employee(1)
        self.assertTrue(result)
        self.assertEqual(get_employees_count(), initial_count - 1)

        # Проверяем, что сотрудник действительно удален
        employee = get_employee_by_id(1)
        self.assertIsNone(employee)

        # Пытаемся удалить несуществующего сотрудника
        result = remove_employee(999)
        self.assertFalse(result)

    def test_remove_employee_invalid_type(self):
        """Тест удаления сотрудника с неправильным типом ID"""
        with self.assertRaises(TypeError):
            remove_employee("invalid")

    @patch('builtins.print')
    def test_update_employee_data(self, mock_print):
        """Тест обновления данных сотрудника"""
        updated = update_employee_data(1, name="Иванов Иван Иванович", salary=130000)

        self.assertIsNotNone(updated)
        self.assertEqual(updated['name'], "Иванов Иван Иванович")
        self.assertEqual(updated['salary'], 130000)

        # Проверяем, что изменения сохранились
        employee = get_employee_by_id(1)
        self.assertEqual(employee['name'], "Иванов Иван Иванович")

    def test_update_employee_data_invalid(self):
        """Тест обновления с некорректными данными"""
        with self.assertRaises(ValueError):
            update_employee_data(1, name="")

        with self.assertRaises(ValueError):
            update_employee_data(1, salary=-1000)

    @patch('builtins.print')
    def test_get_employees_by_position(self, mock_print):
        """Тест получения сотрудников по должности"""
        programmers = get_employees_by_position("Программист")

        self.assertIsInstance(programmers, list)
        self.assertEqual(len(programmers), 1)
        self.assertEqual(programmers[0]['position'], "Программист")

        # Тест с несуществующей должностью
        designers = get_employees_by_position("Дизайнер")
        self.assertEqual(len(designers), 0)

    def test_get_employees_by_position_invalid_type(self):
        """Тест поиска по должности с неправильным типом"""
        with self.assertRaises(TypeError):
            get_employees_by_position(123)

    def test_get_employees_count(self):
        """Тест подсчета количества сотрудников"""
        count = get_employees_count()
        self.assertEqual(count, 3)

        # Добавляем сотрудника и проверяем
        add_employee("Тест", "Тестер")
        new_count = get_employees_count()
        self.assertEqual(new_count, 4)

    @patch('builtins.print')
    def test_clear_employees_db(self, mock_print):
        """Тест очистки базы данных"""
        clear_employees_db()
        count = get_employees_count()
        self.assertEqual(count, 0)

    @patch('builtins.print')
    def test_reset_employees_db(self, mock_print):
        """Тест сброса базы данных"""
        # Изменяем базу
        add_employee("Тест", "Тестер")
        self.assertGreater(get_employees_count(), 3)

        # Сбрасываем
        reset_employees_db()
        count = get_employees_count()
        self.assertEqual(count, 3)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        reset_employees_db()

    @patch('builtins.print')
    def test_full_workflow(self, mock_print):
        """Тест полного рабочего процесса"""
        # 1. Получаем сотрудников
        employees = get_employees()
        self.assertEqual(len(employees), 3)

        # 2. Добавляем нового сотрудника
        new_employee = add_employee("Тестов Т.Т.", "Тестировщик", 110000)
        self.assertIsNotNone(new_employee)

        # 3. Проверяем, что количество увеличилось
        self.assertEqual(get_employees_count(), 4)

        # 4. Рассчитываем зарплату для всех
        salary_result = calculate_salary()
        self.assertEqual(salary_result['total_employees'], 4)

        # 5. Обновляем данные сотрудника
        updated = update_employee_data(new_employee['id'], salary=120000)
        self.assertEqual(updated['salary'], 120000)

        # 6. Удаляем сотрудника
        removed = remove_employee(new_employee['id'])
        self.assertTrue(removed)
        self.assertEqual(get_employees_count(), 3)

    @patch('builtins.print')
    def test_salary_calculation_integration(self, mock_print):
        """Тест интеграции расчета зарплаты"""
        # Добавляем сотрудника с известной зарплатой
        test_employee = add_employee("Тест", "Тестер", 100000)

        # Рассчитываем зарплату
        result = calculate_salary()

        # Проверяем, что новый сотрудник включен в расчет
        test_salary_detail = None
        for detail in result['salary_details']:
            if detail['employee_id'] == test_employee['id']:
                test_salary_detail = detail
                break

        self.assertIsNotNone(test_salary_detail)
        self.assertEqual(test_salary_detail['base_salary'], 100000)
        self.assertEqual(test_salary_detail['total'], 110000)  # 100000 + 10% bonus


def run_tests():
    """Запуск всех тестов"""
    # Создаем тестовый набор
    test_suite = unittest.TestSuite()

    # Добавляем тесты
    test_classes = [TestMainModule, TestSalaryModule, TestPeopleModule, TestIntegration]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result


if __name__ == '__main__':
    print("🧪 Запуск unit-тестов для программы 'Бухгалтерия'")
    print("=" * 60)

    result = run_tests()

    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"✅ Пройдено тестов: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Провалено тестов: {len(result.failures)}")
    print(f"💥 Ошибок: {len(result.errors)}")

    if result.failures:
        print("\n❌ ПРОВАЛИВШИЕСЯ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print("\n💥 ОШИБКИ:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    if result.wasSuccessful():
        print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
    else:
        print("\n⚠️ ЕСТЬ ПРОБЛЕМЫ В ТЕСТАХ!")