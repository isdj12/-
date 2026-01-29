"""
Конфигурация pytest для тестов
"""
import pytest


def pytest_configure(config):
    """Настройка pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "web: marks tests as web tests"
    )
