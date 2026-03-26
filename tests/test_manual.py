"""
Тесты написанные человеком (Manual Tests)
Эти тесты проверяют конкретные сценарии работы сайта
"""
import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_homepage_loads():
    """Проверка загрузки главной страницы"""
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert "Тестовый сайт" in response.text

def test_api_status_returns_ok():
    """Проверка что API возвращает статус OK"""
    response = requests.get(f"{BASE_URL}/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'
    assert 'version' in data

def test_api_users_returns_list():
    """Проверка что API возвращает список пользователей"""
    response = requests.get(f"{BASE_URL}/api/users")
    assert response.status_code == 200
    data = response.json()
    assert 'users' in data
    assert len(data['users']) > 0
    assert data['users'][0]['name'] == 'Иван'

def test_api_data_has_temperature():
    """Проверка что API возвращает данные с температурой"""
    response = requests.get(f"{BASE_URL}/api/data")
    assert response.status_code == 200
    data = response.json()
    assert 'data' in data
    assert 'temperature' in data['data']
    assert isinstance(data['data']['temperature'], (int, float))

def test_api_error_returns_500():
    """Проверка что endpoint /api/error возвращает ошибку 500"""
    response = requests.get(f"{BASE_URL}/api/error")
    assert response.status_code == 500

def test_user_email_format():
    """Проверка формата email пользователей"""
    response = requests.get(f"{BASE_URL}/api/users")
    data = response.json()
    for user in data['users']:
        assert '@' in user['email']
        assert '.' in user['email']
