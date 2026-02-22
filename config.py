import os

# Telegram настройки (обязательно)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8570072935:AAGNnayMmRZa9xnkco43NS4hf1aOxSrF2sw')
CHAT_ID = os.getenv('CHAT_ID', '1566108855')

# База данных
DB_PATH = 'test_history.db'

# Отчеты
REPORTS_DIR = './test_reports'
REPORT_FILE = 'report.json'

# AI настройки (Ollama)
USE_AI_ANALYSIS = True
AI_PROVIDER = 'ollama'
AI_MODEL = 'llama3.2'
OLLAMA_BASE_URL = 'http://localhost:11434'

# Путь к проекту (устанавливается при запуске)
PROJECT_PATH = None
