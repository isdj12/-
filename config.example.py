import os

# Telegram Bot Configuration
# Получи токен у @BotFather в Telegram
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BOTFATHER')

# Получи свой Chat ID у @userinfobot в Telegram
CHAT_ID = os.getenv('CHAT_ID', 'ВСТАВЬ_СЮДА_СВОЙ_CHAT_ID')

# Database Configuration
DB_PATH = 'test_history.db'

# Monitoring Configuration
REPORTS_DIR = './test_reports'
REPORT_FILE = 'report.json'
