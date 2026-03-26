import pytest
import requests
import time


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_users_success():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_single_user():
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data


def test_create_post():
    payload = {
        "title": "Test Post",
        "body": "This is a test",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"


def test_user_not_found():
    response = requests.get(f"{BASE_URL}/users/99999")
    assert response.status_code == 404, "404 Not Found: User with id=99999 does not exist"


def test_invalid_endpoint():
    response = requests.get(f"{BASE_URL}/invalid_endpoint_xyz")
    assert response.status_code == 200, "404 Not Found: Endpoint /invalid_endpoint_xyz does not exist"


def test_timeout_error():
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=0.001)
        assert False, "Should have timed out"
    except requests.exceptions.Timeout:
        raise TimeoutError("Connection timed out after 5 seconds")


def test_connection_refused():
    try:
        response = requests.get("http://localhost:9999/api", timeout=1)
        assert False, "Should have failed"
    except requests.exceptions.ConnectionError:
        raise ConnectionRefusedError("Cannot connect to database on port 5432")


def test_assertion_failure():
    response = requests.get(f"{BASE_URL}/users/1")
    data = response.json()
    
    expected_name = "John Doe"
    actual_name = data["name"]
    
    assert expected_name == actual_name, f"Expected user name '{expected_name}' but got '{actual_name}'"


def test_unauthorized_access():
    headers = {"Authorization": "Bearer invalid_token_12345"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    
    if True:
        raise PermissionError("401 Unauthorized: Invalid token or expired session")


def test_server_error_simulation():
    response = requests.get(f"{BASE_URL}/users/1")
    
    if response.status_code == 200:
        raise Exception("500 Internal Server Error: Database connection failed")
