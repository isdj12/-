"""
Реальные тесты для проверки работы системы мониторинга
Тестируем публичный API JSONPlaceholder
"""
import pytest
import requests
import time


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_users_success():
    """Успешный тест - получение списка пользователей"""
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_single_user():
    """Успешный тест - получение одного пользователя"""
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data


def test_create_post():
    """Успешный тест - создание поста"""
    payload = {
        "title": "Test Post",
        "body": "This is a test",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"


def test_user_not_found():
    """Тест с ошибкой 404 - пользователь не найден"""
    response = requests.get(f"{BASE_URL}/users/99999")
    # Этот API возвращает 200 с пустым объектом, но мы симулируем 404
    assert response.status_code == 404, "404 Not Found: User with id=99999 does not exist"


def test_invalid_endpoint():
    """Тест с ошибкой - неверный endpoint"""
    response = requests.get(f"{BASE_URL}/invalid_endpoint_xyz")
    assert response.status_code == 200, "404 Not Found: Endpoint /invalid_endpoint_xyz does not exist"


def test_timeout_error():
    """Симуляция timeout ошибки"""
    try:
        # Устанавливаем очень короткий таймаут
        response = requests.get(f"{BASE_URL}/users", timeout=0.001)
        assert False, "Should have timed out"
    except requests.exceptions.Timeout:
        raise TimeoutError("Connection timed out after 5 seconds")


def test_connection_refused():
    """Симуляция ошибки подключения"""
    try:
        # Пытаемся подключиться к несуществующему хосту
        response = requests.get("http://localhost:9999/api", timeout=1)
        assert False, "Should have failed"
    except requests.exceptions.ConnectionError:
        raise ConnectionRefusedError("Cannot connect to database on port 5432")


def test_assertion_failure():
    """Тест с assertion ошибкой"""
    response = requests.get(f"{BASE_URL}/users/1")
    data = response.json()
    
    expected_name = "John Doe"
    actual_name = data["name"]
    
    assert expected_name == actual_name, f"Expected user name '{expected_name}' but got '{actual_name}'"


def test_unauthorized_access():
    """Симуляция ошибки авторизации"""
    # Симулируем запрос с неверным токеном
    headers = {"Authorization": "Bearer invalid_token_12345"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    
    # Принудительно вызываем ошибку
    if True:  # API не требует авторизации, но мы симулируем
        raise PermissionError("401 Unauthorized: Invalid token or expired session")


def test_server_error_simulation():
    """Симуляция ошибки сервера 500"""
    response = requests.get(f"{BASE_URL}/users/1")
    
    # Симулируем серверную ошибку
    if response.status_code == 200:
        raise Exception("500 Internal Server Error: Database connection failed")


# Запуск тестов:
# pytest test_simulation/test_api.py --json-report --json-report-file=test_reports/report.json -v
