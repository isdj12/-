@echo off
chcp 65001 >nul
echo ========================================
echo   Загрузка проекта на GitHub
echo ========================================
echo.

echo [1/7] Настройка Git...
git config --global user.email "test@example.com"
git config --global user.name "Test Monitor"

echo.
echo [2/7] Инициализация Git репозитория...
git init

echo.
echo [3/7] Добавление файлов...
git add .

echo.
echo [4/7] Создание коммита...
git commit -m "Initial commit: Test monitoring system"

echo.
echo [5/7] Переименование ветки в main...
git branch -M main

echo.
echo [6/7] Добавление удаленного репозитория...
git remote add origin https://github.com/isdj12/-.git

echo.
echo [7/7] Загрузка на GitHub...
git push -u origin main

echo.
echo ========================================
echo   Готово!
echo ========================================
echo.
echo Проверь репозиторий: https://github.com/isdj12/-
echo.
pause
