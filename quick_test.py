#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрая проверка исправлений
"""

import sys
import os


def test_imports():
    """Проверка импортов всех модулей"""
    print("🔍 Проверка импортов...")

    try:
        # Проверяем основные модули
        import main
        print("✅ main.py")

        from application import salary
        print("✅ application.salary")

        from application.db import people
        print("✅ application.db.people")

        # Проверяем тестовые модули
        import test_accounting
        print("✅ test_accounting.py")

        import test_yandex_disk_api
        print("✅ test_yandex_disk_api.py")

        import test_yandex_selenium
        print("✅ test_yandex_selenium.py")

        print("\n🎉 Все модули импортируются без ошибок!")
        return True

    except SyntaxError as e:
        print(f"❌ Синтаксическая ошибка: {e}")
        return False
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Другая ошибка: {e}")
        return False


def test_basic_functions():
    """Тест базовых функций"""
    print("\n🧪 Проверка базовых функций...")

    try:
        from main import get_program_info, validate_employee_data
        from application.salary import calculate_individual_salary
        from application.db.people import get_employees_count, add_employee

        # Тест программной информации
        info = get_program_info()
        assert isinstance(info, dict)
        print("✅ get_program_info работает")

        # Тест валидации
        is_valid, msg = validate_employee_data({'id': 1, 'name': 'Тест', 'position': 'Тестер'})
        assert is_valid
        print("✅ validate_employee_data работает")

        # Тест расчета зарплаты
        salary = calculate_individual_salary(100000, 10)
        assert salary['total_salary'] == 110000
        print("✅ calculate_individual_salary работает")

        # Тест базы данных
        count = get_employees_count()
        assert isinstance(count, int)
        print("✅ get_employees_count работает")

        print("\n🎉 Все базовые функции работают корректно!")
        return True

    except Exception as e:
        print(f"❌ Ошибка в функциях: {e}")
        return False


def test_api_class():
    """Тест API класса"""
    print("\n🌐 Проверка API класса...")

    try:
        from test_yandex_disk_api import YandexDiskAPI

        # Создаем экземпляр API
        api = YandexDiskAPI("test_token")

        # Проверяем атрибуты
        assert api.token == "test_token"
        assert "cloud-api.yandex.net" in api.base_url
        assert "OAuth test_token" in api.headers['Authorization']

        print("✅ YandexDiskAPI класс инициализируется корректно")
        print("\n🎉 API класс работает!")
        return True

    except Exception as e:
        print(f"❌ Ошибка в API классе: {e}")
        return False


def main():
    """Основная функция быстрой проверки"""
    print("⚡ БЫСТРАЯ ПРОВЕРКА ИСПРАВЛЕНИЙ")
    print("=" * 40)

    results = []

    # Проверяем импорты
    results.append(test_imports())

    # Проверяем функции
    results.append(test_basic_functions())

    # Проверяем API
    results.append(test_api_class())

    # Итоги
    passed = sum(results)
    total = len(results)

    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"✅ Прошло: {passed}/{total}")
    print(f"❌ Провалилось: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ! Можно запускать полные тесты.")
    else:
        print("\n⚠️ ЕСТЬ ПРОБЛЕМЫ. Нужно исправить ошибки.")

    return passed == total


if __name__ == '__main__':
    main()