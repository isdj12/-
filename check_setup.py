#!/usr/bin/env python3
"""
Проверка готовности AI-МОЗГА к работе
"""
import os
import sys

print("🧠 Проверка AI-МОЗГА")
print("=" * 60)

errors = []
warnings = []

# 1. Проверка config.py
print("\n1️⃣ Проверка config.py...")
if not os.path.exists('config.py'):
    errors.append("config.py не найден! Скопируй config.example.py в config.py")
else:
    try:
        import config
        if 'YOUR_BOT_TOKEN' in config.BOT_TOKEN:
            errors.append("BOT_TOKEN не настроен в config.py")
        else:
            print("   ✓ BOT_TOKEN настроен")
        
        if 'YOUR_CHAT_ID' in config.CHAT_ID:
            errors.append("CHAT_ID не настроен в config.py")
        else:
            print("   ✓ CHAT_ID настроен")
        
        print(f"   ✓ AI_PROVIDER: {config.AI_PROVIDER}")
        print(f"   ✓ AI_MODEL: {config.AI_MODEL}")
    except Exception as e:
        errors.append(f"Ошибка импорта config.py: {e}")

# 2. Проверка зависимостей
print("\n2️⃣ Проверка зависимостей...")
required = ['aiogram', 'watchdog', 'pytest', 'requests']
for module in required:
    try:
        __import__(module)
        print(f"   ✓ {module}")
    except ImportError:
        errors.append(f"{module} не установлен. Запусти: pip install {module}")

# 3. Проверка Ollama
print("\n3️⃣ Проверка Ollama...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print("   ✓ Ollama запущен")
        if models:
            print("   ✓ Доступные модели:")
            for model in models:
                print(f"      - {model['name']}")
        else:
            warnings.append("Нет загруженных моделей. Запусти: ollama pull llama3.2")
    else:
        warnings.append("Ollama не отвечает. Запусти: ollama serve")
except Exception as e:
    warnings.append(f"Ollama недоступен: {e}. Запусти: ollama serve")

# 4. Проверка структуры
print("\n4️⃣ Проверка структуры...")
if os.path.exists('tests'):
    print("   ✓ tests/")
    test_files = [f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]
    if test_files:
        print(f"   ✓ Найдено тестов: {len(test_files)}")
    else:
        warnings.append("В tests/ нет файлов test_*.py")
else:
    warnings.append("Папка tests/ не найдена")

if os.path.exists('.gitignore'):
    print("   ✓ .gitignore")
else:
    warnings.append(".gitignore не найден")

# 5. Итоги
print("\n" + "=" * 60)

if errors:
    print("\n❌ ОШИБКИ:")
    for error in errors:
        print(f"   • {error}")

if warnings:
    print("\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
    for warning in warnings:
        print(f"   • {warning}")

if not errors and not warnings:
    print("\n✅ ВСЕ ГОТОВО!")
    print("\n📝 Следующие шаги:")
    print("   1. python3 ai_brain.py")
    print("   2. Открой Telegram")
    print("   3. Отправь /start боту")
    print("   4. Жми 🚀 Запустить тесты")
elif not errors:
    print("\n✅ Готово к запуску (есть предупреждения)")
    print("\n📝 Можешь запустить: python3 ai_brain.py")
else:
    print("\n❌ Исправь ошибки перед запуском")
    sys.exit(1)

print()
