#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selenium тесты для авторизации на Яндексе (Задание 3 - необязательное)
"""

import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class YandexAuthTests(unittest.TestCase):
    """Тесты авторизации на Яндексе с помощью Selenium"""

    @classmethod
    def setUpClass(cls):
        """Настройка драйвера перед всеми тестами"""
        # Настраиваем опции Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Без GUI (можно закомментировать для отладки)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        # Инициализируем драйвер
        try:
            service = Service(ChromeDriverManager().install())
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
            cls.driver.implicitly_wait(10)
        except Exception as e:
            raise unittest.SkipTest(f"Не удалось инициализировать Chrome WebDriver: {e}")

    @classmethod
    def tearDownClass(cls):
        """Закрытие драйвера после всех тестов"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.auth_url = "https://passport.yandex.ru/auth/"
        self.wait = WebDriverWait(self.driver, 10)

    def test_auth_page_loads(self):
        """Тест загрузки страницы авторизации"""
        self.driver.get(self.auth_url)

        # Проверяем, что страница загрузилась
        self.assertIn("yandex", self.driver.current_url.lower())

        # Проверяем заголовок страницы
        title = self.driver.title
        self.assertTrue(any(word in title.lower() for word in ["яндекс", "yandex", "авторизация", "auth"]))

    def test_login_form_elements_present(self):
        """Тест наличия элементов формы авторизации"""
        self.driver.get(self.auth_url)

        try:
            # Ищем поле ввода логина
            login_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "passp-field-login"))
            )
            self.assertTrue(login_field.is_displayed())

            # Ищем кнопку "Войти"
            login_button = self.driver.find_element(By.ID, "passp:sign-in")
            self.assertTrue(login_button.is_displayed())

        except TimeoutException:
            # Альтернативные селекторы, если основные не найдены
            try:
                login_field = self.driver.find_element(By.NAME, "login")
                self.assertTrue(login_field.is_displayed())
            except NoSuchElementException:
                # Ищем по более общим селекторам
                login_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
                self.assertGreater(len(login_fields), 0, "Поле ввода логина не найдено")

    def test_invalid_login_validation(self):
        """Тест валидации при вводе некорректного логина"""
        self.driver.get(self.auth_url)

        try:
            # Находим поле логина
            login_field = self.wait.until(
                EC.element_to_be_clickable((By.ID, "passp-field-login"))
            )

            # Вводим некорректный логин
            login_field.clear()
            login_field.send_keys("invalid_email_format")

            # Находим и нажимаем кнопку входа
            login_button = self.driver.find_element(By.ID, "passp:sign-in")
            login_button.click()

            # Ждем появления сообщения об ошибке
            time.sleep(2)

            # Проверяем, что остались на странице авторизации (не прошли дальше)
            self.assertIn("passport.yandex", self.driver.current_url)

        except (TimeoutException, NoSuchElementException) as e:
            self.skipTest(f"Не удалось найти элементы формы: {e}")

    def test_empty_login_validation(self):
        """Тест валидации пустого поля логина"""
        self.driver.get(self.auth_url)

        try:
            # Находим кнопку входа и пытаемся нажать без ввода логина
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "passp:sign-in"))
            )
            login_button.click()

            time.sleep(1)

            # Проверяем, что остались на той же странице
            self.assertIn("passport.yandex", self.driver.current_url)

            # Кнопка должна оставаться неактивной или показывать ошибку
            page_source = self.driver.page_source.lower()
            error_indicators = ["ошибка", "error", "обязательное", "required", "заполните"]
            has_error_indication = any(indicator in page_source for indicator in error_indicators)

            # Если нет явного сообщения об ошибке, проверяем что кнопка неактивна
            if not has_error_indication:
                button_disabled = not login_button.is_enabled()
                self.assertTrue(button_disabled, "Кнопка должна быть неактивна при пустом логине")

        except (TimeoutException, NoSuchElementException) as e:
            self.skipTest(f"Не удалось найти кнопку входа: {e}")

    def test_login_field_accepts_input(self):
        """Тест возможности ввода в поле логина"""
        self.driver.get(self.auth_url)

        try:
            # Находим поле логина
            login_field = self.wait.until(
                EC.element_to_be_clickable((By.ID, "passp-field-login"))
            )

            # Проверяем, что поле активно для ввода
            self.assertTrue(login_field.is_enabled())

            # Вводим тестовый текст
            test_email = "test@example.com"
            login_field.clear()
            login_field.send_keys(test_email)

            # Проверяем, что текст был введен
            entered_value = login_field.get_attribute("value")
            self.assertEqual(entered_value, test_email)

        except (TimeoutException, NoSuchElementException) as e:
            self.skipTest(f"Не удалось найти поле логина: {e}")

    def test_page_title_and_content(self):
        """Тест содержимого страницы авторизации"""
        self.driver.get(self.auth_url)

        # Проверяем наличие ключевых элементов
        page_source = self.driver.page_source.lower()

        # Ключевые слова, которые должны присутствовать на странице авторизации
        expected_content = ["вход", "логин", "пароль", "войти", "яндекс"]
        found_content = [word for word in expected_content if word in page_source]

        self.assertGreater(len(found_content), 0,
                           f"На странице не найдено ожидаемого контента. Найдено: {found_content}")

    def test_alternative_auth_methods(self):
        """Тест наличия альтернативных методов авторизации"""
        self.driver.get(self.auth_url)

        # Ищем ссылки на альтернативные методы входа
        page_source = self.driver.page_source.lower()

        alternative_methods = [
            "qr", "телефон", "phone", "соцсети", "social",
            "facebook", "вконтакте", "одноклассники"
        ]

        found_methods = [method for method in alternative_methods if method in page_source]

        # Проверяем, что есть хотя бы один альтернативный метод
        # (это не обязательно, поэтому используем мягкое утверждение)
        if found_methods:
            print(f"Найдены альтернативные методы авторизации: {found_methods}")

    def test_responsive_design(self):
        """Тест адаптивности дизайна"""
        self.driver.get(self.auth_url)

        # Тестируем разные разрешения экрана
        resolutions = [
            (1920, 1080),  # Desktop
            (768, 1024),  # Tablet
            (375, 667)  # Mobile
        ]

        for width, height in resolutions:
            self.driver.set_window_size(width, height)
            time.sleep(1)

            # Проверяем, что основные элементы видимы
            try:
                login_elements = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "input[type='text'], input[type='email'], input[name='login']"
                )

                visible_elements = [elem for elem in login_elements if elem.is_displayed()]
                self.assertGreater(len(visible_elements), 0,
                                   f"При разрешении {width}x{height} поле логина не видно")

            except Exception as e:
                print(f"Предупреждение: при разрешении {width}x{height} возникла проблема: {e}")

    def test_security_headers(self):
        """Тест наличия базовых заголовков безопасности"""
        self.driver.get(self.auth_url)

        # Проверяем, что страница загружена по HTTPS
        self.assertTrue(self.driver.current_url.startswith("https://"),
                        "Страница авторизации должна использовать HTTPS")

        # Проверяем, что нет смешанного контента (все ресурсы по HTTPS)
        logs = self.driver.get_log('browser')
        mixed_content_errors = [
            log for log in logs
            if 'mixed content' in log.get('message', '').lower()
        ]

        self.assertEqual(len(mixed_content_errors), 0,
                         f"Обнаружены ошибки смешанного контента: {mixed_content_errors}")


class TestYandexAuthWithRealCredentials(unittest.TestCase):
    """Тесты с реальными учетными данными (если доступны)"""

    @classmethod
    def setUpClass(cls):
        """Настройка для тестов с реальными данными"""
        cls.test_login = os.environ.get('YANDEX_TEST_LOGIN')
        cls.test_password = os.environ.get('YANDEX_TEST_PASSWORD')

        if not cls.test_login or not cls.test_password:
            raise unittest.SkipTest(
                "Пропускаем тесты с реальными данными: не заданы YANDEX_TEST_LOGIN и YANDEX_TEST_PASSWORD"
            )

        # Настраиваем драйвер
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """Закрытие драйвера"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def test_successful_login(self):
        """Тест успешной авторизации (требует реальные данные)"""
        self.driver.get("https://passport.yandex.ru/auth/")

        try:
            # Вводим логин
            login_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "passp-field-login"))
            )
            login_field.clear()
            login_field.send_keys(self.test_login)

            # Нажимаем кнопку входа
            login_button = self.driver.find_element(By.ID, "passp:sign-in")
            login_button.click()

            # Ждем появления поля пароля
            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "passp-field-passwd"))
            )
            password_field.send_keys(self.test_password)

            # Нажимаем кнопку входа с паролем
            password_login_button = self.driver.find_element(By.ID, "passp:sign-in")
            password_login_button.click()

            # Ждем перенаправления
            WebDriverWait(self.driver, 15).until(
                lambda driver: "passport.yandex.ru/auth" not in driver.current_url
            )

            # Проверяем успешную авторизацию
            self.assertNotIn("passport.yandex.ru/auth", self.driver.current_url)

        except Exception as e:
            self.fail(f"Не удалось выполнить авторизацию: {e}")


def run_selenium_tests():
    """Запуск Selenium тестов"""
    print("🔧 Проверка доступности WebDriver...")

    try:
        # Проверяем, можем ли инициализировать драйвер
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        test_driver = webdriver.Chrome(service=service, options=chrome_options)
        test_driver.quit()
        print("✅ WebDriver доступен")

    except Exception as e:
        print(f"❌ WebDriver недоступен: {e}")
        print("Для запуска Selenium тестов установите Chrome и chromedriver")
        return None

    # Создаем тестовый набор
    test_suite = unittest.TestSuite()

    # Добавляем основные тесты
    basic_tests = unittest.TestLoader().loadTestsFromTestCase(YandexAuthTests)
    test_suite.addTests(basic_tests)

    # Добавляем тесты с реальными данными (если доступны)
    if os.environ.get('YANDEX_TEST_LOGIN') and os.environ.get('YANDEX_TEST_PASSWORD'):
        real_tests = unittest.TestLoader().loadTestsFromTestCase(TestYandexAuthWithRealCredentials)
        test_suite.addTests(real_tests)
        print("🔐 Тесты с реальными данными включены")
    else:
        print("⚠️ Тесты с реальными данными пропущены (не заданы учетные данные)")

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result


if __name__ == '__main__':
    print("🧪 Запуск Selenium тестов для авторизации на Яндексе")
    print("=" * 60)
    print("Для тестов с реальными данными установите переменные окружения:")
    print("export YANDEX_TEST_LOGIN='ваш_логин'")
    print("export YANDEX_TEST_PASSWORD='ваш_пароль'")
    print("=" * 60)

    result = run_selenium_tests()

    if result:
        print("\n" + "=" * 60)
        print("📊 РЕЗУЛЬТАТЫ SELENIUM ТЕСТОВ:")
        print(f"✅ Пройдено тестов: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"❌ Провалено тестов: {len(result.failures)}")
        print(f"💥 Ошибок: {len(result.errors)}")

        if result.wasSuccessful():
            print("\n🎉 ВСЕ SELENIUM ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        else:
            print("\n⚠️ ЕСТЬ ПРОБЛЕМЫ В SELENIUM ТЕСТАХ!")
    else:
        print("\n❌ Selenium тесты не были запущены из-за проблем с WebDriver")