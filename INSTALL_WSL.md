# Установка AI-МОЗГА в WSL

## 1. Скопируй проект в WSL

В Windows PowerShell:
```powershell
wsl
cd ~
```

Скопируй папку проекта в домашнюю директорию WSL.

## 2. Запусти автоустановку

```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

Скрипт автоматически:
- Обновит систему
- Установит Python
- Установит зависимости
- Установит Ollama
- Загрузит модель llama3.2

## 3. Включи AI в config.py

```python
USE_AI_ANALYSIS = True
```

## 4. Запусти AI-мозг

```bash
python3 ai_brain.py
```

## 5. В другом терминале запусти Ollama (если не запущен)

```bash
ollama serve
```

Готово! Теперь AI-мозг работает с локальной нейронкой!
