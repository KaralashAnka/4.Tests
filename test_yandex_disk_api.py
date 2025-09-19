#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit-тесты для Яндекс.Диск REST API
"""

import unittest
import requests
import json
from unittest.mock import patch, MagicMock
import time
import os


class YandexDiskAPI:
    """Класс для работы с API Яндекс.Диска"""

    def __init__(self, token):
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {
            'Authorization': f'OAuth {token}',
            'Content-Type': 'application/json'
        }

    def create_folder(self, path):
        """
        Создать папку на Яндекс.Диске

        Args:
            path (str): Путь к папке

        Returns:
            dict: Ответ API
        """
        url = f"{self.base_url}/resources"
        params = {'path': path}

        response = requests.put(url, headers=self.headers, params=params)

        return {
            'status_code': response.status_code,
            'response': response.json() if response.content else {}
        }

    def get_folder_info(self, path):
        """
        Получить информацию о папке

        Args:
            path (str): Путь к папке

        Returns:
            dict: Информация о папке
        """
        url = f"{self.base_url}/resources"
        params = {'path': path}

        response = requests.get(url, headers=self.headers, params=params)

        return {
            'status_code': response.status_code,
            'response': response.json() if response.content else {}
        }

    def delete_folder(self, path):
        """
        Удалить папку с Яндекс.Диска

        Args:
            path (str): Путь к папке

        Returns:
            dict: Ответ API
        """
        url = f"{self.base_url}/resources"
        params = {'path': path, 'permanently': 'true'}

        response = requests.delete(url, headers=self.headers, params=params)

        return {
            'status_code': response.status_code,
            'response': response.json() if response.content else {}
        }

    def list_files(self, path="/"):
        """
        Получить список файлов и папок

        Args:
            path (str): Путь для просмотра

        Returns:
            dict: Список файлов и папок
        """
        url = f"{self.base_url}/resources"
        params = {'path': path}

        response = requests.get(url, headers=self.headers, params=params)

        return {
            'status_code': response.status_code,
            'response': response.json() if response.content else {}
        }


class TestYandexDiskAPI(unittest.TestCase):
    """Тесты для API Яндекс.Диска"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        # Используем тестовый токен (в реальности должен быть настоящий)
        self.test_token = "test_token_123456"
        self.api = YandexDiskAPI(self.test_token)
        self.test_folder_path = "/test_folder_for_unittest"

    @patch('requests.put')
    def test_create_folder_success(self, mock_put):
        """Тест успешного создания папки"""
        # Мокаем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = True
        mock_response.json.return_value = {
            "href": "https://cloud-api.yandex.net/v1/disk/resources?path=%2Ftest_folder",
            "method": "GET",
            "templated": False
        }
        mock_put.return_value = mock_response

        # Выполняем тест
        result = self.api.create_folder(self.test_folder_path)

        # Проверки
        self.assertEqual(result['status_code'], 201)
        self.assertIn('href', result['response'])

        # Проверяем, что был вызван правильный URL
        mock_put.assert_called_once()
        call_args = mock_put.call_args
        # Проверяем позиционные аргументы (URL передается первым аргументом)
        called_url = call_args[0][0] if call_args[0] else ""
        self.assertIn('cloud-api.yandex.net', called_url)

    @patch('requests.put')
    def test_create_folder_already_exists(self, mock_put):
        """Тест создания папки, которая уже существует"""
        # Мокаем ответ об ошибке
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_response.content = True
        mock_response.json.return_value = {
            "message": "Specified path already exists.",
            "description": "Resource already exists.",
            "error": "DiskPathPointsToExistentDirectoryError"
        }
        mock_put.return_value = mock_response

        # Выполняем тест
        result = self.api.create_folder(self.test_folder_path)

        # Проверки
        self.assertEqual(result['status_code'], 409)
        self.assertIn('error', result['response'])
        self.assertEqual(result['response']['error'], 'DiskPathPointsToExistentDirectoryError')

    @patch('requests.put')
    def test_create_folder_unauthorized(self, mock_put):
        """Тест создания папки с неправильным токеном"""
        # Мокаем ответ об ошибке авторизации
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.content = True
        mock_response.json.return_value = {
            "message": "Unauthorized",
            "description": "Unauthorized",
            "error": "UnauthorizedError"
        }
        mock_put.return_value = mock_response

        # Выполняем тест
        result = self.api.create_folder(self.test_folder_path)

        # Проверки
        self.assertEqual(result['status_code'], 401)
        self.assertIn('error', result['response'])
        self.assertEqual(result['response']['error'], 'UnauthorizedError')

    @patch('requests.put')
    def test_create_folder_invalid_path(self, mock_put):
        """Тест создания папки с некорректным путем"""
        # Мокаем ответ об ошибке пути
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.content = True
        mock_response.json.return_value = {
            "message": "Specified path is invalid.",
            "description": "Path contains invalid characters.",
            "error": "DiskPathFormatError"
        }
        mock_put.return_value = mock_response

        # Выполняем тест с некорректным путем
        result = self.api.create_folder("/invalid<>path")

        # Проверки
        self.assertEqual(result['status_code'], 400)
        self.assertIn('error', result['response'])
        self.assertEqual(result['response']['error'], 'DiskPathFormatError')

    @patch('requests.get')
    def test_get_folder_info_success(self, mock_get):
        """Тест успешного получения информации о папке"""
        # Мокаем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = True
        mock_response.json.return_value = {
            "name": "test_folder_for_unittest",
            "type": "dir",
            "path": "disk:/test_folder_for_unittest",
            "created": "2024-01-01T12:00:00+00:00",
            "modified": "2024-01-01T12:00:00+00:00"
        }
        mock_get.return_value = mock_response

        # Выполняем тест
        result = self.api.get_folder_info(self.test_folder_path)

        # Проверки
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['response']['type'], 'dir')
        self.assertEqual(result['response']['name'], 'test_folder_for_unittest')

    @patch('requests.get')
    def test_get_folder_info_not_found(self, mock_get):
        """Тест получения информации о несуществующей папке"""
        # Мокаем ответ об ошибке
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = True
        mock_response.json.return_value = {
            "message": "Resource not found.",
            "description": "Resource not found.",
            "error": "DiskNotFoundError"
        }
        mock_get.return_value = mock_response

        # Выполняем тест
        result = self.api.get_folder_info("/nonexistent_folder")

        # Проверки
        self.assertEqual(result['status_code'], 404)
        self.assertIn('error', result['response'])
        self.assertEqual(result['response']['error'], 'DiskNotFoundError')

    @patch('requests.get')
    def test_list_files_success(self, mock_get):
        """Тест успешного получения списка файлов"""
        # Мокаем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = True
        mock_response.json.return_value = {
            "type": "dir",
            "name": "/",
            "path": "disk:/",
            "_embedded": {
                "items": [
                    {
                        "name": "test_folder_for_unittest",
                        "type": "dir",
                        "path": "disk:/test_folder_for_unittest"
                    },
                    {
                        "name": "example.txt",
                        "type": "file",
                        "path": "disk:/example.txt"
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        # Выполняем тест
        result = self.api.list_files("/")

        # Проверки
        self.assertEqual(result['status_code'], 200)
        self.assertIn('_embedded', result['response'])
        self.assertIn('items', result['response']['_embedded'])

        items = result['response']['_embedded']['items']
        self.assertGreater(len(items), 0)

        # Проверяем, что наша тестовая папка есть в списке
        folder_found = False
        for item in items:
            if item['name'] == 'test_folder_for_unittest' and item['type'] == 'dir':
                folder_found = True
                break

        self.assertTrue(folder_found, "Тестовая папка должна быть в списке файлов")

    @patch('requests.delete')
    def test_delete_folder_success(self, mock_delete):
        """Тест успешного удаления папки"""
        # Мокаем успешный ответ
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = False
        mock_response.json.return_value = {}
        mock_delete.return_value = mock_response

        # Выполняем тест
        result = self.api.delete_folder(self.test_folder_path)

        # Проверки
        self.assertEqual(result['status_code'], 204)

        # Проверяем, что был вызван DELETE запрос
        mock_delete.assert_called_once()

    def test_api_headers(self):
        """Тест правильности заголовков API"""
        expected_headers = {
            'Authorization': f'OAuth {self.test_token}',
            'Content-Type': 'application/json'
        }

        self.assertEqual(self.api.headers, expected_headers)

    def test_api_base_url(self):
        """Тест правильности базового URL"""
        expected_url = "https://cloud-api.yandex.net/v1/disk"
        self.assertEqual(self.api.base_url, expected_url)


class TestYandexDiskAPIIntegration(unittest.TestCase):
    """Интеграционные тесты для API (требуют настоящий токен)"""

    def setUp(self):
        """Подготовка для интеграционных тестов"""
        # Получаем токен из переменной окружения
        self.token = os.environ.get('YANDEX_DISK_TOKEN')

        if not self.token:
            self.skipTest("Пропускаем интеграционные тесты: не задан YANDEX_DISK_TOKEN")

        self.api = YandexDiskAPI(self.token)
        self.test_folder_path = f"/test_folder_{int(time.time())}"

    def test_full_folder_lifecycle(self):
        """Тест полного жизненного цикла папки (создание, проверка, удаление)"""
        # 1. Создаем папку
        create_result = self.api.create_folder(self.test_folder_path)
        self.assertIn(create_result['status_code'], [201, 409])  # 201 - создана, 409 - уже существует

        # 2. Проверяем, что папка создалась
        info_result = self.api.get_folder_info(self.test_folder_path)
        self.assertEqual(info_result['status_code'], 200)
        self.assertEqual(info_result['response']['type'], 'dir')

        # 3. Проверяем, что папка появилась в списке
        list_result = self.api.list_files("/")
        self.assertEqual(list_result['status_code'], 200)

        folder_name = self.test_folder_path.split('/')[-1]
        items = list_result['response']['_embedded']['items']
        folder_found = any(
            item['name'] == folder_name and item['type'] == 'dir'
            for item in items
        )
        self.assertTrue(folder_found, "Созданная папка должна появиться в списке файлов")

        # 4. Удаляем папку
        delete_result = self.api.delete_folder(self.test_folder_path)
        self.assertIn(delete_result['status_code'], [204, 202])  # 204 - удалена, 202 - в процессе

        # 5. Проверяем, что папка удалилась
        time.sleep(1)  # Ждем немного для завершения удаления
        info_after_delete = self.api.get_folder_info(self.test_folder_path)
        self.assertEqual(info_after_delete['status_code'], 404)


def run_api_tests():
    """Запуск тестов API"""
    # Создаем тестовый набор
    test_suite = unittest.TestSuite()

    # Добавляем юнит-тесты (с моками)
    unit_tests = unittest.TestLoader().loadTestsFromTestCase(TestYandexDiskAPI)
    test_suite.addTests(unit_tests)

    # Добавляем интеграционные тесты (только если есть токен)
    if os.environ.get('YANDEX_DISK_TOKEN'):
        integration_tests = unittest.TestLoader().loadTestsFromTestCase(TestYandexDiskAPIIntegration)
        test_suite.addTests(integration_tests)
        print("🔗 Интеграционные тесты включены (найден YANDEX_DISK_TOKEN)")
    else:
        print("⚠️ Интеграционные тесты пропущены (не задан YANDEX_DISK_TOKEN)")

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result


if __name__ == '__main__':
    print("🧪 Запуск тестов для Яндекс.Диск API")
    print("=" * 60)
    print("Для запуска интеграционных тестов установите переменную окружения:")
    print("export YANDEX_DISK_TOKEN='ваш_токен'")
    print("=" * 60)

    result = run_api_tests()

    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ API:")
    print(f"✅ Пройдено тестов: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Провалено тестов: {len(result.failures)}")
    print(f"💥 Ошибок: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n🎉 ВСЕ ТЕСТЫ API ПРОШЛИ УСПЕШНО!")
    else:
        print("\n⚠️ ЕСТЬ ПРОБЛЕМЫ В ТЕСТАХ API!")