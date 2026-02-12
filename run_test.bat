@echo off
chcp 65001 >nul
echo ========================================
echo   ЗАПУСК ТЕСТОВ
echo ========================================
echo.

echo ВАЖНО: Убедись что мониторинг запущен!
echo Если нет - запусти в другом терминале: python monitor.py
echo.

echo [1/2] Создание папки для отчетов...
if not exist test_reports mkdir test_reports

echo.
echo [2/2] Запуск тестов...
echo.
echo Использование:
echo   pytest твои_тесты.py --json-report --json-report-file=test_reports/report.json -v
echo.
echo Замени "твои_тесты.py" на имя твоего файла с тестами
echo.
pause
