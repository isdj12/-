import os

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
CHAT_ID = os.getenv('CHAT_ID', 'YOUR_CHAT_ID_HERE')

# Database Configuration
DB_PATH = 'test_history.db'

# Monitoring Configuration
REPORTS_DIR = './test_reports'
REPORT_FILE = 'report.json'
