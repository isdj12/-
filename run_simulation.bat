@echo off
echo ========================================
echo   Запуск симуляции тестирования
echo ========================================
echo.

echo [1/3] Проверка зависимостей...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Устанавливаю requests...
    pip install requests
)

pip show pytest >nul 2>&1
if errorlevel 1 (
    echo Устанавливаю pytest...
    pip install pytest pytest-json-report
)

echo.
echo [2/3] Создание папки для отчетов...
if not exist test_reports mkdir test_reports

echo.
echo [3/3] Запуск тестов...
echo.
pytest test_simulation/ --json-report --json-report-file=test_reports/report.json -v

echo.
echo ========================================
echo   Тесты завершены!
echo   Отчет сохранен в: test_reports\report.json
echo ========================================
echo.
echo Теперь можешь:
echo 1. Запустить мониторинг: python watcher.py
echo 2. Или проанализировать отчет: python main.py test_reports\report.json
echo.
pause
