# Быстрый старт

## Шаг 1: Настройка бота (5 минут)

1. **Создай бота в Telegram:**
   - Открой Telegram и найди @BotFather
   - Отправь команду `/newbot`
   - Придумай имя (например: `My Test Monitor Bot`)
   - Придумай username (например: `my_test_monitor_bot`)
   - Скопируй полученный токен (выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Узнай свой Chat ID:**
   - Найди в Telegram бота @userinfobot
   - Отправь ему любое сообщение
   - Скопируй свой ID (число, например: `123456789`)

3. **Настрой config.py:**
   Открой файл `config.py` и замени:
   ```python
   BOT_TOKEN = 'твой_токен_от_BotFather'
   CHAT_ID = 'твой_chat_id'
   ```

## Шаг 2: Установка (2 минуты)

```bash
pip install -r requirements.txt
```

## Шаг 3: Проверка работы (1 минута)

### Windows:
```bash
run_simulation.bat
```

### Linux/Mac:
```bash
chmod +x run_simulation.sh
./run_simulation.sh
```

Это запустит тесты и создаст отчет в `test_reports/report.json`

## Шаг 4: Запуск системы

### Вариант А: Демонстрация (без Telegram)
```bash
python demo.py
```
Покажет анализ в консоли без отправки в Telegram.

### Вариант Б: Автоматический мониторинг
Запусти в одном терминале:
```bash
python monitor.py
```

Теперь система будет автоматически следить за папкой `test_reports/` и отправлять уведомления при появлении новых отчетов.

В другом терминале запусти тесты:
```bash
pytest test_simulation/ --json-report --json-report-file=test_reports/report.json -v
```

### Вариант В: Ручной анализ
```bash
python monitor.py test_reports/report.json
```

## Готово!

Теперь в Telegram должны прийти уведомления о результатах тестов!

## Использование бота

Напиши боту `/start` и используй кнопки:
- **Последний отчет** — статистика за 24 часа
- **Топ проблем** — самые падающие тесты
- **Что проверить?** — общие рекомендации

## Интеграция с твоими тестами

Добавь в команду запуска своих тестов:
```bash
pytest твои_тесты/ --json-report --json-report-file=test_reports/report.json && python monitor.py test_reports/report.json
```

Или просто запусти `python monitor.py` один раз, и он будет следить за всеми новыми отчетами автоматически!

## Проблемы?

1. **Бот не отвечает** → Проверь токен в `config.py`
2. **Нет уведомлений** → Проверь Chat ID в `config.py`
3. **Ошибка импорта** → Установи зависимости: `pip install -r requirements.txt`
4. **Тесты не запускаются** → Установи: `pip install requests pytest pytest-json-report`
