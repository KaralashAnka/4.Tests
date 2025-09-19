#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск всех тестов для домашнего задания по тестированию
"""

import sys
import os
import subprocess
import time
from datetime import datetime


def print_header(title):
    """Печать заголовка"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)


def print_section(title):
    """Печать секции"""
    print(f"\n📋 {title}")
    print("-" * 40)


def check_dependencies():
    """Проверка зависимостей"""
    print_section("Проверка зависимостей")

    required_modules = [
        'unittest', 'requests', 'selenium', 'webdriver_manager'
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - НЕ УСТАНОВЛЕН")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n⚠️ Отсутствующие модули: {', '.join(missing_modules)}")
        print("Установите зависимости: pip install -r requirements_tests.txt")
        return False

    print("\n✅ Все зависимости установлены")
    return True


def run_unit_tests():
    """Запуск unit-тестов для бухгалтерии"""
    print_header("ЗАДАНИЕ 1: Unit-тесты программы 'Бухгалтерия'")

    try:
        # Запускаем тесты бухгалтерии
        result = subprocess.run([
            sys.executable, 'test_accounting.py'
        ], capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')

        print("📤 ВЫВОД ТЕСТОВ:")
        if result.stdout:
            print(result.stdout)
        else:
            print("(Нет вывода)")

        if result.stderr:
            print("⚠️ ПРЕДУПРЕЖДЕНИЯ/ОШИБКИ:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Unit-тесты бухгалтерии прошли успешно!")
            return True
        else:
            print(f"❌ Unit-тесты завершились с кодом {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Тесты превысили время ожидания (60 сек)")
        return False
    except Exception as e:
        print(f"💥 Ошибка при запуске unit-тестов: {e}")
        return False


def run_api_tests():
    """Запуск тестов API Яндекс.Диска"""
    print_header("ЗАДАНИЕ 2: Тесты API Яндекс.Диска")

    try:
        # Запускаем API тесты
        result = subprocess.run([
            sys.executable, 'test_yandex_disk_api.py'
        ], capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')

        print("📤 ВЫВОД API ТЕСТОВ:")
        if result.stdout:
            print(result.stdout)
        else:
            print("(Нет вывода)")

        if result.stderr:
            print("⚠️ ПРЕДУПРЕЖДЕНИЯ/ОШИБКИ:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ API тесты прошли успешно!")
            return True
        else:
            print(f"❌ API тесты завершились с кодом {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("⏰ API тесты превысили время ожидания (60 сек)")
        return False
    except Exception as e:
        print(f"💥 Ошибка при запуске API тестов: {e}")
        return False


def run_selenium_tests():
    """Запуск Selenium тестов"""
    print_header("ЗАДАНИЕ 3: Selenium тесты авторизации Яндекса")

    try:
        # Запускаем Selenium тесты
        result = subprocess.run([
            sys.executable, 'test_yandex_selenium.py'
        ], capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace')

        print("📤 ВЫВОД SELENIUM ТЕСТОВ:")
        if result.stdout:
            print(result.stdout)
        else:
            print("(Нет вывода)")

        if result.stderr:
            print("⚠️ ПРЕДУПРЕЖДЕНИЯ/ОШИБКИ:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Selenium тесты прошли успешно!")
            return True
        else:
            print(f"❌ Selenium тесты завершились с кодом {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Selenium тесты превысили время ожидания (120 сек)")
        return False
    except Exception as e:
        print(f"💥 Ошибка при запуске Selenium тестов: {e}")
        return False


def check_test_files():
    """Проверка наличия файлов тестов"""
    print_section("Проверка файлов тестов")

    required_files = [
        'test_accounting.py',
        'test_yandex_disk_api.py',
        'test_yandex_selenium.py',
        'main.py',
        'application/salary.py',
        'application/db/people.py'
    ]

    missing_files = []

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - НЕ НАЙДЕН")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n⚠️ Отсутствующие файлы: {', '.join(missing_files)}")
        return False

    print("\n✅ Все файлы тестов найдены")
    return True


def show_environment_info():
    """Показать информацию об окружении"""
    print_section("Информация об окружении")

    print(f"🐍 Python: {sys.version}")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    print(f"🕐 Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Проверяем переменные окружения для интеграционных тестов
    env_vars = [
        'YANDEX_DISK_TOKEN',
        'YANDEX_TEST_LOGIN',
        'YANDEX_TEST_PASSWORD'
    ]

    print("\n🔐 Переменные окружения для интеграционных тестов:")
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: ***установлена***")
        else:
            print(f"⚪ {var}: не установлена")


def generate_test_report(results):
    """Генерация отчета о тестировании"""
    print_header("ИТОГОВЫЙ ОТЧЕТ")

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests

    print(f"📊 Общая статистика:")
    print(f"   Всего наборов тестов: {total_tests}")
    print(f"   ✅ Прошли успешно: {passed_tests}")
    print(f"   ❌ Провалились: {failed_tests}")
    print(f"   📈 Успешность: {(passed_tests / total_tests) * 100:.1f}%")

    print(f"\n📋 Детальные результаты:")
    for test_name, result in results.items():
        status = "✅ ПРОШЕЛ" if result else "❌ ПРОВАЛИЛСЯ"
        print(f"   {test_name}: {status}")

    # Рекомендации
    print(f"\n💡 Рекомендации:")
    if failed_tests == 0:
        print("   🎉 Отлично! Все тесты прошли успешно!")
        print("   📚 Домашнее задание выполнено полностью.")
    else:
        print("   🔧 Проверьте провалившиеся тесты")
        print("   📖 Убедитесь, что все зависимости установлены")
        if not results.get('API тесты', True):
            print("   🔑 Для API тестов нужен токен Яндекс.Диска")
        if not results.get('Selenium тесты', True):
            print("   🌐 Для Selenium тестов нужен Chrome браузер")


def main():
    """Основная функция запуска всех тестов"""
    print("🚀 ЗАПУСК ВСЕХ ТЕСТОВ ДОМАШНЕГО ЗАДАНИЯ")
    print("Лекция 4: «Tests»")

    # Показываем информацию об окружении
    show_environment_info()

    # Проверяем файлы
    if not check_test_files():
        print("\n❌ Не все файлы найдены. Завершение.")
        return

    # Проверяем зависимости
    if not check_dependencies():
        print("\n❌ Не все зависимости установлены. Завершение.")
        return

    # Запускаем тесты
    start_time = time.time()
    results = {}

    # 1. Unit-тесты бухгалтерии
    results['Unit-тесты бухгалтерии'] = run_unit_tests()

    # 2. API тесты Яндекс.Диска
    results['API тесты'] = run_api_tests()

    # 3. Selenium тесты (необязательно)
    results['Selenium тесты'] = run_selenium_tests()

    # Подсчитываем время выполнения
    end_time = time.time()
    execution_time = end_time - start_time

    # Генерируем отчет
    generate_test_report(results)

    print(f"\n⏱️ Общее время выполнения: {execution_time:.2f} секунд")
    print(f"🕐 Завершено в: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()