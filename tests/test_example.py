"""
Пример теста для AI-МОЗГА
Создавай свои тесты в этой папке
"""
import requests

def test_example_website():
    """Пример теста проверки сайта"""
    # Замени на свой URL
    response = requests.get("https://httpbin.org/status/200")
    assert response.status_code == 200, "Сайт недоступен"

def test_example_json():
    """Пример теста API"""
    response = requests.get("https://httpbin.org/json")
    assert response.status_code == 200
    data = response.json()
    assert 'slideshow' in data
