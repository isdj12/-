Основной модуль: парсер, анализатор и база данных

import json
import sqlite3
import re
from datetime import datetime
from config import DB_PATH, REPORTS_DIR, REPORT_FILE
import os

# АНАЛИЗАТОР ОШИБОК

ERROR_RECOMMENDATIONS = {
    'timeout': {
        'keywords': ['timeout', 'timed out', 'time limit exceeded'],
        'diagnosis': 'Превышено время ожидания ответа',
        'recommendations': [
            'Проверь нагрузку на сервер',
            'Убедись, что сервис доступен',
            'Проверь стабильность сети',
            'Увеличь таймаут в конфигурации теста'
        ]
    },
    'connection': {
        'keywords': ['connection refused', 'connection error', 'cannot connect'],
        'diagnosis': 'Ошибка подключения к сервису',
        'recommendations': [
            'Проверь, запущен ли сервер',
            'Убедись, что порт доступен',
            'Проверь настройки firewall',
            'Проверь правильность URL/хоста'
        ]
    },
    'auth': {
        'keywords': ['unauthorized', '401', 'authentication failed', 'invalid token'],
        'diagnosis': 'Проблема с аутентификацией',
        'recommendations': [
            'Проверь валидность токена',
            'Убедись, что учетные данные актуальны',
            'Проверь срок действия сессии',
            'Проверь права доступа пользователя'
        ]
    },
    'not_found': {
        'keywords': ['404', 'not found', 'does not exist'],
        'diagnosis': 'Ресурс не найден',
        'recommendations': [
            'Проверь правильность URL',
            'Убедись, что ресурс существует в БД',
            'Проверь миграции базы данных',
            'Проверь роутинг приложения'
        ]
    },
    'server_error': {
        'keywords': ['500', 'internal server error', 'server error'],
        'diagnosis': 'Внутренняя ошибка сервера',
        'recommendations': [
            'Проверь логи сервера',
            'Проверь состояние базы данных',
            'Убедись, что все зависимости доступны',
            'Проверь конфигурацию сервера'
        ]
    },
    'assertion': {
        'keywords': ['assertion', 'expected', 'actual'],
        'diagnosis': 'Несоответствие ожидаемого и фактического результата',
        'recommendations': [
            'Проверь тестовые данные',
            'Убедись, что логика приложения не изменилась',
            'Проверь актуальность тестовых ожиданий',
            'Воспроизведи сценарий вручную'
        ]
    }
}


class ErrorAnalyzer:
    @staticmethod
    def analyze_error(error_message):
        if not error_message:
            return None
        
        error_lower = error_message.lower()
        
        for error_type, error_info in ERROR_RECOMMENDATIONS.items():
            for keyword in error_info['keywords']:
                if keyword in error_lower:
                    return {
                        'type': error_type,
                        'diagnosis': error_info['diagnosis'],
                        'recommendations': error_info['recommendations']
                    }
        
        return {
            'type': 'unknown',
            'diagnosis': 'Неизвестная ошибка',
            'recommendations': [
                'Изучи полный текст ошибки в логах',
                'Попробуй воспроизвести проблему вручную',
                'Проверь последние изменения в коде'
            ]
        }
    
    @staticmethod
    def get_severity(failure_count):
        if failure_count >= 3:
            return '[КРИТИЧНО]'
        elif failure_count >= 2:
            return '[ВНИМАНИЕ]'
        else:
            return '[РАЗОВАЯ ОШИБКА]'


# ПАРСЕР ОТЧЕТОВ

class ReportParser:
    @staticmethod
    def parse_pytest_json(report_path):
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            results = []
            tests = data.get('tests', [])
            
            for test in tests:
                test_info = {
                    'name': test.get('nodeid', 'Unknown'),
                    'status': 'PASSED' if test.get('outcome') == 'passed' else 'FAILED',
                    'error_message': None
                }
                
                if test_info['status'] == 'FAILED':
                    call_info = test.get('call', {})
                    test_info['error_message'] = call_info.get('longrepr', 'No error details')
                
                results.append(test_info)
            
            return results
        except Exception as e:
            print(f"Ошибка парсинга отчета: {e}")
            return []
    
    @staticmethod
    def get_latest_report():
        report_path = os.path.join(REPORTS_DIR, REPORT_FILE)
        if os.path.exists(report_path):
            return report_path
        return None


# БАЗА ДАННЫХ

class TestDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                error_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_test_result(self, test_name, status, error_message=None, error_type=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO test_runs (test_name, status, error_message, error_type)
            VALUES (?, ?, ?, ?)
        ''', (test_name, status, error_message, error_type))
        self.conn.commit()
    
    def get_test_failure_count(self, test_name, days=7):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM test_runs
            WHERE test_name = ? AND status = 'FAILED'
            AND timestamp >= datetime('now', '-' || ? || ' days')
        ''', (test_name, days))
        return cursor.fetchone()[0]
    
    def get_top_failing_tests(self, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT test_name, COUNT(*) as fail_count
            FROM test_runs
            WHERE status = 'FAILED'
            AND timestamp >= datetime('now', '-7 days')
            GROUP BY test_name
            ORDER BY fail_count DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def get_last_run_summary(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM test_runs
            WHERE timestamp >= datetime('now', '-1 day')
            GROUP BY status
        ''')
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()
