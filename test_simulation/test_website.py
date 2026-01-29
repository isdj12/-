"""
Тесты для проверки работы реального сайта
Используем requests для простоты (без Selenium)
"""
import pytest
import requests


def test_google_homepage():
    """Проверка доступности Google"""
    response = requests.get("https://www.google.com", timeout=5)
    assert response.status_code == 200
    assert "google" in response.text.lower()


def test_github_api():
    """Проверка GitHub API"""
    response = requests.get("https://api.github.com", timeout=5)
    assert response.status_code == 200


def test_httpbin_status_codes():
    """Тест различных HTTP статусов"""
    # Успешный запрос
    response = requests.get("https://httpbin.org/status/200")
    assert response.status_code == 200


def test_httpbin_404():
    """Тест 404 ошибки"""
    response = requests.get("https://httpbin.org/status/404")
    assert response.status_code == 200, "404 Not Found: Resource does not exist"


def test_httpbin_500():
    """Тест 500 ошибки"""
    response = requests.get("https://httpbin.org/status/500")
    assert response.status_code == 200, "500 Internal Server Error: Server encountered an error"


def test_httpbin_delay_timeout():
    """Тест с задержкой - симуляция timeout"""
    try:
        # Запрашиваем задержку 10 секунд, но таймаут 2 секунды
        response = requests.get("https://httpbin.org/delay/10", timeout=2)
        assert False, "Should have timed out"
    except requests.exceptions.Timeout:
        raise TimeoutError("Request timed out after 2 seconds")


def test_invalid_url():
    """Тест с неверным URL"""
    try:
        response = requests.get("https://this-domain-does-not-exist-12345.com", timeout=3)
        assert False, "Should have failed"
    except requests.exceptions.RequestException:
        raise ConnectionError("Cannot connect to host: DNS resolution failed")


def test_httpbin_json_response():
    """Проверка JSON ответа"""
    response = requests.get("https://httpbin.org/json")
    assert response.status_code == 200
    data = response.json()
    
    # Специально неверное ожидание для демонстрации
    assert data.get("slideshow", {}).get("title") == "Wrong Title", \
        f"Expected 'Wrong Title' but got '{data.get('slideshow', {}).get('title')}'"


# Запуск:
# pytest test_simulation/test_website.py --json-report --json-report-file=test_reports/report.json -v
