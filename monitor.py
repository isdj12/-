"""
Мониторинг и анализ тестов
"""
import asyncio
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import ReportParser, ErrorAnalyzer, TestDatabase
from telegram_bot import TesterBot


def load_config():
    """Загружает конфигурацию мониторинга"""
    try:
        with open('monitor_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если конфига нет - используем настройки по умолчанию
        from config import REPORTS_DIR, REPORT_FILE
        return {
            'test_folder': os.getcwd(),
            'reports_dir': REPORTS_DIR,
            'report_file': REPORT_FILE
        }


class ReportHandler(FileSystemEventHandler):
    """Обработчик событий файловой системы"""
    
    def __init__(self, bot, db, report_file):
        self.bot = bot
        self.db = db
        self.report_file = report_file
    
    def on_modified(self, event):
        """Вызывается при изменении файла"""
        if event.src_path.endswith(self.report_file):
            print(f"Обнаружен новый отчет: {event.src_path}")
            asyncio.run(self.process_report(event.src_path))
    
    async def process_report(self, report_path):
        """Обрабатывает отчет о тестах"""
        # Парсим отчет
        results = ReportParser.parse_pytest_json(report_path)
        
        for test in results:
            error_info = None
            error_type = None
            
            # Если тест упал - анализируем ошибку
            if test['status'] == 'FAILED':
                error_info = ErrorAnalyzer.analyze_error(test['error_message'])
                error_type = error_info['type'] if error_info else None
            
            # Сохраняем в БД
            self.db.add_test_result(
                test['name'],
                test['status'],
                test['error_message'],
                error_type
            )
            
            # Получаем количество падений
            failure_count = self.db.get_test_failure_count(test['name'])
            
            # Отправляем уведомление в Telegram
            await self.bot.send_test_notification(
                test['name'],
                test['status'],
                error_info,
                failure_count
            )


class TestMonitor:
    """Главный класс мониторинга"""
    
    def __init__(self, config=None):
        if config is None:
            config = load_config()
        
        self.config = config
        self.db = TestDatabase()
        self.bot = TesterBot()
        self.observer = Observer()
    
    def start(self):
        """Запускает мониторинг"""
        reports_dir = self.config['reports_dir']
        report_file = self.config['report_file']
        
        # Создаем папку для отчетов если её нет
        os.makedirs(reports_dir, exist_ok=True)
        
        # Настраиваем обработчик событий
        event_handler = ReportHandler(self.bot, self.db, report_file)
        self.observer.schedule(event_handler, reports_dir, recursive=False)
        self.observer.start()
        
        print(f"Мониторинг запущен")
        print(f"Папка с тестами: {self.config['test_folder']}")
        print(f"Папка с отчетами: {reports_dir}")
        print("Нажми Ctrl+C для остановки")
        
        try:
            asyncio.run(self.bot.start_polling())
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Останавливает мониторинг"""
        self.observer.stop()
        self.observer.join()
        self.db.close()
        print("\nМониторинг остановлен")


async def analyze_report(report_path):
    """Анализ одного отчета без мониторинга"""
    db = TestDatabase()
    bot = TesterBot()
    
    print(f"Анализирую отчет: {report_path}")
    results = ReportParser.parse_pytest_json(report_path)
    
    for test in results:
        error_info = None
        error_type = None
        
        if test['status'] == 'FAILED':
            error_info = ErrorAnalyzer.analyze_error(test['error_message'])
            error_type = error_info['type'] if error_info else None
        
        db.add_test_result(
            test['name'],
            test['status'],
            test['error_message'],
            error_type
        )
        
        failure_count = db.get_test_failure_count(test['name'])
        
        await bot.send_test_notification(
            test['name'],
            test['status'],
            error_info,
            failure_count
        )
    
    await bot.close()
    db.close()
    print("Анализ завершен")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Режим анализа конкретного файла
        report_path = sys.argv[1]
        asyncio.run(analyze_report(report_path))
    else:
        # Режим непрерывного мониторинга
        monitor = TestMonitor()
        monitor.start()
