#!/bin/bash

echo "🧠 AI-МОЗГ - Полный запуск"
echo "=========================="
echo ""

PROJECT_DIR=$(pwd)

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено"
    echo "Создай: python -m venv venv"
    exit 1
fi

# Проверка Ollama
if [ ! -f "ollama_local/ollama" ]; then
    echo "❌ Ollama не установлена"
    echo "Запусти: ./install_ollama_local.sh"
    exit 1
fi

# Проверка модели
if [ ! -d "ollama_data/manifests" ] || [ -z "$(ls -A ollama_data/manifests 2>/dev/null)" ]; then
    echo "⚠️ Модель llama3.2 не загружена"
    echo ""
    echo "Запускаю Ollama для загрузки модели..."
    ./start_ollama.sh &
    OLLAMA_PID=$!
    sleep 5
    
    echo "📥 Загружаю модель llama3.2 (это займет время)..."
    ./ollama_local/pull_model.sh
    
    kill $OLLAMA_PID 2>/dev/null
    sleep 2
fi

echo "✓ Все проверки пройдены"
echo ""

# Запуск Ollama в фоне
echo "🚀 Запускаю Ollama..."
./start_ollama.sh > /dev/null 2>&1 &
OLLAMA_PID=$!
echo "✓ Ollama запущена (PID: $OLLAMA_PID)"

# Ждем запуска Ollama
sleep 3

# Опционально запускаем сайт
read -p "Запустить тестовый сайт? (y/n): " START_WEBSITE
if [ "$START_WEBSITE" = "y" ]; then
    echo "🌐 Запускаю сайт..."
    source venv/bin/activate
    python website/app.py > /dev/null 2>&1 &
    WEBSITE_PID=$!
    echo "✓ Сайт запущен на http://127.0.0.1:5000 (PID: $WEBSITE_PID)"
fi

echo ""
echo "🧠 Запускаю AI-МОЗГ..."
echo "=========================="
echo ""

# Активируем venv и запускаем AI-МОЗГ
source venv/bin/activate
python ai_brain.py

# При выходе убиваем процессы
echo ""
echo "🛑 Останавливаю процессы..."
kill $OLLAMA_PID 2>/dev/null
[ ! -z "$WEBSITE_PID" ] && kill $WEBSITE_PID 2>/dev/null
echo "✓ Готово"
