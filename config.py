import os

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8570072935:AAGNnayMmRZa9xnkco43NS4hf1aOxSrF2sw')
CHAT_ID = os.getenv('CHAT_ID', '1566108855')

# Database Configuration
DB_PATH = 'test_history.db'

# Monitoring Configuration
REPORTS_DIR = './test_reports'
REPORT_FILE = 'report.json'
