"""
Мониторинг и анализ тестов
"""
import asyncio
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import ReportParser, ErrorAnalyzer, TestDatabase
from telegram_bot import TesterBot
from config import REPORTS_DIR, REPORT_FILE


class ReportHandler(FileSystemEventHandler):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def on_modified(self, event):
        if event.src_path.endswith(REPORT_FILE):
            print(f"Обнаружен новый отчет: {event.src_path}")
            asyncio.run(self.process_report(event.src_path))
    
    async def process_report(self, report_path):
        results = ReportParser.parse_pytest_json(report_path)
        
        for test in results:
            error_info = None
            error_type = None
            
            if test['status'] == 'FAILED':
                error_info = ErrorAnalyzer.analyze_error(test['error_message'])
                error_type = error_info['type'] if error_info else None
            
            self.db.add_test_result(
                test['name'],
                test['status'],
                test['error_message'],
                error_type
            )
            
            failure_count = self.db.get_test_failure_count(test['name'])
            
            await self.bot.send_test_notification(
                test['name'],
                test['status'],
                error_info,
                failure_count
            )


class TestMonitor:
    def __init__(self):
        self.db = TestDatabase()
        self.bot = TesterBot()
        self.observer = Observer()
    
    def start(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        event_handler = ReportHandler(self.bot, self.db)
        self.observer.schedule(event_handler, REPORTS_DIR, recursive=False)
        self.observer.start()
        
        print(f"Мониторинг запущен. Слежу за папкой: {REPORTS_DIR}")
        print("Нажми Ctrl+C для остановки")
        
        try:
            asyncio.run(self.bot.start_polling())
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
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
