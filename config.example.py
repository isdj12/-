import os

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
CHAT_ID = os.getenv('CHAT_ID', 'YOUR_CHAT_ID_HERE')

DB_PATH = 'test_history.db'

REPORTS_DIR = './test_reports'
REPORT_FILE = 'report.json'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
USE_AI_ANALYSIS = os.getenv('USE_AI_ANALYSIS', 'false').lower() == 'true'
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4o-mini')

TEST_FOLDERS = {
    'basic': 'tests',
    'website': 'my_tests',
    'user': 'user_tests',
    'all': '.'
}

DEFAULT_TEST_FOLDER = 'all'
