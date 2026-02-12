# Умный Telegram-мониторинг тестов

Интеллектуальная система мониторинга и оперативного анализа тестирования с уведомлениями в Telegram.

---

## Быстрый старт (3 шага)

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка Telegram бота
Скопируй `config.example.py` в `config.py`:
```bash
copy config.example.py config.py
```

Отредактируй `config.py`:
```python
BOT_TOKEN = 'твой_токен_от_BotFather'  # Получи у @BotFather
CHAT_ID = 'твой_chat_id'                # Получи у @userinfobot
```

### 3. Настройка папки с тестами
```bash
python setup_monitor.py
```
Выбери папку где находятся твои тесты.

### 4. Запуск мониторинга
```bash
python monitor.py
```

### 5. Запуск тестов
```bash
pytest твои_тесты/ --json-report --json-report-file=test_reports/report.json
```

Готово! Уведомления придут в Telegram автоматически.

---

## Быстрый тест системы

Создай свой тестовый файл (например `test_my_app.py`) и запусти:
```bash
pytest test_my_app.py --json-report --json-report-file=test_reports/report.json -v
```

Или используй шаблон `run_test.bat` для быстрого запуска.

---

## Что делает система

Система автоматически:
- Следит за результатами тестов
- Анализирует причины падений
- Выдает конкретные рекомендации
- Отправляет уведомления в Telegram
- Ведет историю для выявления системных проблем

### Распознает 6 типов ошибок:
1. **timeout** - превышение времени ожидания
2. **connection** - ошибки подключения
3. **auth** - проблемы аутентификации (401)
4. **not_found** - ресурс не найден (404)
5. **server_error** - ошибки сервера (500)
6. **assertion** - несоответствие ожиданий

Для каждой ошибки выдает:
- Понятный диагноз
- Конкретные рекомендации
- Уровень критичности

---

## Структура проекта

```
├── config.py              # Настройки (токен бота, пути)
├── core.py                # Ядро: парсер + анализатор + БД
├── telegram_bot.py        # Telegram бот
├── monitor.py             # Мониторинг
├── setup_monitor.py       # Настройка папки с тестами
├── demo.py                # Демо без Telegram
├── run_test.bat           # Шаблон для запуска тестов
└── requirements.txt       # Зависимости
```

---

## Команды бота в Telegram

После запуска напиши боту `/start` и используй кнопки:
- **Последний отчет** - статистика за 24 часа
- **Топ проблем** - самые падающие тесты за неделю
- **Что проверить?** - общие рекомендации
- **Очистить БД** - удалить всю историю тестов

---

## Режимы работы

### Режим 1: Демонстрация (без Telegram)
```bash
python demo.py
```
Покажет анализ последнего отчета в консоли.

### Режим 2: Непрерывный мониторинг
```bash
python monitor.py
```
Следит за папкой `test_reports` постоянно.

### Режим 3: Анализ конкретного отчета
```bash
python monitor.py путь/к/report.json
```

---

## Интеграция с pytest

Добавь в команду запуска тестов:
```bash
pytest твои_тесты/ --json-report --json-report-file=test_reports/report.json
```

Или создай `pytest.ini`:
```ini
[pytest]
addopts = --json-report --json-report-file=test_reports/report.json
```

Теперь просто запускай:
```bash
pytest
```

---

## Пример уведомления в Telegram

```
[ВНИМАНИЕ]

[FAIL] Упал тест: test_user_login

Диагноз: Превышено время ожидания ответа

Что проверить:
1. Проверь нагрузку на сервер
2. Убедись, что сервис доступен
3. Проверь стабильность сети
4. Увеличь таймаут в конфигурации теста

[!] Тест падал 2 раз за последние 7 дней
```

---

## База данных

Все результаты сохраняются в SQLite (`test_history.db`):
- История всех прогонов
- Статистика падений
- Типы ошибок
- Временные метки

---

## Расширение функционала

### Добавление нового типа ошибки

Отредактируй `core.py`, добавь в словарь `ERROR_RECOMMENDATIONS`:

```python
ERROR_RECOMMENDATIONS['memory_error'] = {
    'keywords': ['out of memory', 'memory error', 'oom'],
    'diagnosis': 'Недостаточно памяти',
    'recommendations': [
        'Проверь использование памяти',
        'Увеличь лимит памяти для процесса',
        'Оптимизируй работу с данными'
    ]
}
```

---

## Как работает система

### 1. Парсер (ReportParser)
Читает JSON отчет pytest и извлекает:
- Имя теста
- Статус (PASSED/FAILED)
- Текст ошибки

### 2. Анализатор (ErrorAnalyzer)
Ищет ключевые слова в тексте ошибки:
- "timeout" → диагноз + рекомендации по timeout
- "404" → диагноз + рекомендации по not_found
- "connection" → диагноз + рекомендации по connection
- и т.д.

### 3. База данных (TestDatabase)
Сохраняет каждый прогон:
- Для отслеживания повторяющихся проблем
- Для статистики
- Для определения критичности

### 4. Telegram бот (TesterBot)
Отправляет уведомления:
- При каждом упавшем тесте
- С диагнозом и рекомендациями
- С историей падений

---

## Устранение проблем

### "No module named 'watchdog'"
```bash
pip install watchdog
```

### "No module named 'aiogram'"
```bash
pip install aiogram
```

### "Token is invalid"
Проверь токен в `config.py` - должен быть от @BotFather.

### Мониторинг не видит отчеты
1. Запусти `python setup_monitor.py`
2. Проверь путь в `monitor_config.json`
3. Убедись что тесты сохраняют отчет в `test_reports/report.json`

---

## Требования

- Python 3.8+
- Telegram аккаунт
- pytest (для генерации отчетов)

---

## Примеры использования

### Пример 1: Первый запуск
```bash
# 1. Установка
pip install -r requirements.txt

# 2. Настройка бота (отредактируй config.py)
# BOT_TOKEN = 'твой_токен'
# CHAT_ID = 'твой_id'

# 3. Настройка папки
python setup_monitor.py

# 4. Запуск мониторинга
python monitor.py

# 5. В другом терминале - запуск тестов
pytest твои_тесты.py --json-report --json-report-file=test_reports/report.json -v
```

### Пример 2: Ежедневное использование
```bash
# Запускаешь мониторинг один раз
python monitor.py

# Работаешь как обычно
pytest --json-report --json-report-file=test_reports/report.json

# Получаешь уведомления автоматически
```

### Пример 3: Без Telegram
```bash
# Запускаешь тесты
pytest твои_тесты.py --json-report --json-report-file=test_reports/report.json -v

# Смотришь анализ в консоли
python demo.py
```

---

## Полезные команды

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка папки с тестами
python setup_monitor.py

# Запуск мониторинга
python monitor.py

# Демонстрация без Telegram
python demo.py

# Быстрый тест
run_test.bat

# Запуск своих тестов
pytest твои_тесты/ --json-report --json-report-file=test_reports/report.json

# Просмотр конфига
type monitor_config.json  # Windows
cat monitor_config.json   # Linux/Mac
```

---

## Лицензия

MIT License

---

## Автор

Система мониторинга тестов с Telegram интеграцией
