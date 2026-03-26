import asyncio
import os
import subprocess
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, CHAT_ID
from core import ReportParser, AIErrorAnalyzer, TestDatabase


class AIBrain:
    
    def __init__(self, project_path=None):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.db = TestDatabase()
        self.ai_analyzer = AIErrorAnalyzer()
        self.project_path = project_path or os.getcwd()
        self.is_running_tests = False
        self.current_test_folder = 'tests'  # По умолчанию папка tests
        self.setup_handlers()
        
        print("🧠 AI-МОЗГ ИНИЦИАЛИЗИРОВАН")
        print(f"📁 Проект: {self.project_path}")
        print(f"📱 Telegram Chat ID: {CHAT_ID}")
        print(f"🧪 Папка с тестами: {self.current_test_folder}")
    
    def setup_handlers(self):
        
        @self.dp.message(Command('start'))
        async def cmd_start(message: types.Message):
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Запустить тесты")],
                    [KeyboardButton(text="AI сканирование сайта")],
                    [KeyboardButton(text="Последний отчет"), KeyboardButton(text="Топ проблем")],
                    [KeyboardButton(text="AI анализ"), KeyboardButton(text="Статистика")],
                    [KeyboardButton(text="Очистить БД")]
                ],
                resize_keyboard=True
            )
            await message.answer(
                f"AI-МОЗГ АКТИВИРОВАН\n\n"
                f"Проект: {self.project_path}\n"
                f"Папка тестов: {self.current_test_folder}\n\n"
                f"Команды:\n"
                f"Запустить тесты - запуск всех тестов\n"
                f"AI сканирование - нейронка проанализирует сайт\n"
                f"Последний отчет - результаты за 24ч\n"
                f"Топ проблем - самые падающие тесты\n"
                f"AI анализ - глубокий анализ через Ollama\n"
                f"Статистика - общая статистика",
                reply_markup=keyboard
            )
        
        @self.dp.message()
        async def handle_message(message: types.Message):
            if not message.text:
                return
            
            text = message.text.strip()
            
            if text in ["Запустить тесты"]:
                if self.is_running_tests:
                    await message.answer("Тесты уже выполняются, подожди...")
                    return
                await message.answer(f"Запускаю тесты в: {self.project_path}/tests/")
                await self.run_tests_and_analyze()
            
            elif text in ["AI сканирование сайта"]:
                await message.answer("Запускаю AI сканирование сайта...")
                await self.ai_scan_website()
            
            elif text in ["Последний отчет"]:
                await self.send_last_report()
            
            elif text in ["Топ проблем"]:
                await self.send_top_problems()
            
            elif text in ["AI анализ"]:
                await self.send_ai_deep_analysis()
            
            elif text in ["Статистика"]:
                await self.send_statistics()
            
            elif text in ["Очистить БД"]:
                await self.clear_database()
            
            else:
                await message.answer("Неизвестная команда. Используй /start")
        
        @self.dp.callback_query()
        async def handle_callback(callback: types.CallbackQuery):
            await callback.answer()
    
    async def run_tests_and_analyze(self):
        self.is_running_tests = True
        
        try:
            # Создаем папку для отчетов в директории AI-МОЗГА
            ai_mozg_dir = os.path.dirname(os.path.abspath(__file__))
            reports_dir = os.path.join(ai_mozg_dir, 'test_reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            await self.bot.send_message(CHAT_ID, f"Запускаю тесты в проекте:\n{self.project_path}")
            
            # Путь к папке tests в выбранном проекте
            test_path = os.path.join(self.project_path, 'tests')
            report_file = os.path.join(reports_dir, 'report.json')
            
            result = subprocess.run(
                ['pytest', test_path, '--json-report', f'--json-report-file={report_file}', '-v'],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            report_path = report_file
            
            if not os.path.exists(report_path):
                await self.bot.send_message(
                    CHAT_ID,
                    "Отчет не найден\n\n"
                    "Проверь:\n"
                    "1. pytest установлен\n"
                    "2. pytest-json-report установлен\n"
                    "3. папка 'tests' существует в проекте\n"
                    "4. в папке 'tests' есть файлы test_*.py"
                )
                return
            
            await self.analyze_and_send_report(report_path)
            
        except FileNotFoundError:
            await self.bot.send_message(
                CHAT_ID,
                "pytest не найден\n\n"
                "Установи: pip install pytest pytest-json-report"
            )
        except Exception as e:
            await self.bot.send_message(CHAT_ID, f"Ошибка: {str(e)}")
        finally:
            self.is_running_tests = False
    
    async def analyze_and_send_report(self, report_path):
        results = ReportParser.parse_pytest_json(report_path)
        
        if not results:
            await self.bot.send_message(CHAT_ID, "Отчет пустой")
            return
        
        passed = failed = 0
        failed_tests = []
        
        for test in results:
            if test['status'] == 'PASSED':
                passed += 1
            else:
                failed += 1
                
                error_info = self.ai_analyzer.analyze_error(
                    test['error_message'],
                    test['name']
                )
                
                self.db.add_test_result(
                    test['name'],
                    test['status'],
                    test['error_message'],
                    error_info['type'] if error_info else None
                )
                
                failure_count = self.db.get_test_failure_count(test['name'])
                
                failed_tests.append({
                    'test': test,
                    'error_info': error_info,
                    'failure_count': failure_count
                })
        
        summary = f"ОТЧЕТ\n\n"
        summary += f"Успешно: {passed}\n"
        summary += f"Упало: {failed}\n"
        summary += f"все: {len(results)}\n"
        summary += f"Время: {datetime.now().strftime('%H:%M:%S')}\n"
        
        await self.bot.send_message(CHAT_ID, summary)
        
        for item in failed_tests:
            await self.send_test_failure_details(
                item['test'],
                item['error_info'],
                item['failure_count']
            )
    
    async def send_test_failure_details(self, test, error_info, failure_count):
        severity = self.ai_analyzer.get_severity(failure_count)
        
        message = f"{severity}\n\n"
        message += f"Тест: {test['name']}\n\n"
        
        if error_info:
            ai_badge = "AI" if error_info.get('ai_powered') else "Базовый"
            message += f"{ai_badge} Диагноз:\n{error_info['diagnosis']}\n\n"
            message += "Рекомендации:\n"
            for i, rec in enumerate(error_info['recommendations'], 1):
                message += f"{i}. {rec}\n"
            
            if failure_count > 1:
                message += f"\nПадал {failure_count} раз за последние 7 дней"
        
        await self.bot.send_message(CHAT_ID, message)
    
    async def send_last_report(self):
        summary = self.db.get_last_run_summary()
        if not summary:
            await self.bot.send_message(CHAT_ID, "Нет данных за последние 24ч")
            return
        
        text = "Отчет за последние 24ч:\n\n"
        for status, count in summary:
            text += f"{status}: {count}\n"
        
        await self.bot.send_message(CHAT_ID, text)
    
    async def ai_scan_website(self):
        """AI сканирование сайта - нейронка анализирует структуру и проблемы"""
        try:
            import requests
            from urllib.parse import urljoin, urlparse
            
            await self.bot.send_message(CHAT_ID, "Ищу сайт для анализа...")
            
            website_url = None
            app_file = os.path.join(self.project_path, 'app.py')
            
            if os.path.exists(app_file):
                website_url = "http://127.0.0.1:5000"
            
            if not website_url:
                await self.bot.send_message(
                    CHAT_ID,
                    "Сайт не найден\n\n"
                    "Убедись что:\n"
                    "1. Сайт запущен (python website/app.py)\n"
                    "2. Доступен на http://127.0.0.1:5000"
                )
                return
            
            await self.bot.send_message(CHAT_ID, f"Сканирую: {website_url}")
            
            try:
                response = requests.get(website_url, timeout=5)
                status_code = response.status_code
            except Exception as e:
                await self.bot.send_message(
                    CHAT_ID,
                    f"Сайт недоступен\n\n"
                    f"Ошибка: {str(e)}\n\n"
                    f"Запусти сайт: python website/app.py"
                )
                return
            
            await self.bot.send_message(CHAT_ID, "AI анализирует сайт...")
            
            scan_data = {
                'url': website_url,
                'status_code': status_code,
                'content_length': len(response.text),
                'headers': dict(response.headers)
            }
            
            endpoints = []
            if 'api' in response.text.lower():
                endpoints.append('/api/status')
                endpoints.append('/api/users')
                endpoints.append('/api/data')
            
            endpoint_results = []
            for endpoint in endpoints:
                try:
                    ep_response = requests.get(urljoin(website_url, endpoint), timeout=3)
                    endpoint_results.append({
                        'endpoint': endpoint,
                        'status': ep_response.status_code,
                        'ok': ep_response.status_code == 200
                    })
                except:
                    endpoint_results.append({
                        'endpoint': endpoint,
                        'status': 'error',
                        'ok': False
                    })
            
            prompt = f"""Проанализируй сайт и дай краткий отчет:

URL: {website_url}
Статус: {status_code}
Размер: {len(response.text)} байт

Найденные endpoints:
{chr(10).join([f"- {ep['endpoint']}: {ep['status']}" for ep in endpoint_results])}

Дай краткий анализ:
1. Общее состояние сайта
2. Проблемы если есть
3. Рекомендации по улучшению

Ответ на русском, кратко."""

            ai_analysis = self.ai_analyzer.analyze_with_ollama(prompt)
            
            report = f"AI СКАНИРОВАНИЕ САЙТА\n\n"
            report += f"URL: {website_url}\n"
            report += f"Статус: {status_code}\n"
            report += f"Размер: {len(response.text)} байт\n\n"
            
            if endpoint_results:
                report += "Endpoints:\n"
                for ep in endpoint_results:
                    icon = "[OK]" if ep['ok'] else "[ERR]"
                    report += f"{icon} {ep['endpoint']} - {ep['status']}\n"
                report += "\n"
            
            report += f"AI Анализ:\n{ai_analysis}\n"
            
            await self.bot.send_message(CHAT_ID, report)
            
        except Exception as e:
            await self.bot.send_message(CHAT_ID, f"Ошибка сканирования: {str(e)}")
    
    async def send_top_problems(self):
        top_tests = self.db.get_top_failing_tests()
        if not top_tests:
            await self.bot.send_message(CHAT_ID, "Нет падающих тестов за последнюю неделю")
            return
        
        text = "Топ падающих тестов (7 дней):\n\n"
        for i, (test_name, count) in enumerate(top_tests, 1):
            text += f"{i}. {test_name}\n   Падений: {count}\n\n"
        
        await self.bot.send_message(CHAT_ID, text)
    
    async def send_ai_deep_analysis(self):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT test_name, error_message, COUNT(*) as fail_count
            FROM test_runs
            WHERE status = 'FAILED'
            AND timestamp >= datetime('now', '-7 days')
            GROUP BY test_name
            ORDER BY fail_count DESC
            LIMIT 3
        ''')
        
        failed_tests = cursor.fetchall()
        
        if not failed_tests:
            await self.bot.send_message(CHAT_ID, "Нет ошибок для анализа")
            return
        
        await self.bot.send_message(CHAT_ID, "Запускаю глубокий AI анализ...")
        
        for test_name, error_message, fail_count in failed_tests:
            error_info = self.ai_analyzer.analyze_error(error_message, test_name)
            
            message = f"ГЛУБОКИЙ АНАЛИЗ\n\n"
            message += f"Тест: {test_name}\n"
            message += f"Падений: {fail_count}\n\n"
            
            if error_info:
                message += f"AI Диагноз:\n{error_info['diagnosis']}\n\n"
                message += "Рекомендации:\n"
                for i, rec in enumerate(error_info['recommendations'], 1):
                    message += f"{i}. {rec}\n"
            
            await self.bot.send_message(CHAT_ID, message)
    
    async def send_statistics(self):
        cursor = self.db.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM test_runs')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM test_runs WHERE status = "PASSED"')
        passed = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM test_runs WHERE status = "FAILED"')
        failed = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM test_runs
            WHERE timestamp >= datetime('now', '-7 days')
        ''')
        last_week = cursor.fetchone()[0]
        
        text = "СТАТИСТИКА\n\n"
        text += f"всего запусков: {total}\n"
        text += f"Успешно: {passed}\n"
        text += f"Упало: {failed}\n"
        text += f"за последние 7 дней: {last_week}\n"
        
        if total > 0:
            success_rate = (passed / total) * 100
            text += f"\n  процент успеха: {success_rate:.1f}%"
        
        await self.bot.send_message(CHAT_ID, text)
    
    async def clear_database(self):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM test_runs')
        count = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM test_runs')
        self.db.conn.commit()
        
        await self.bot.send_message(
            CHAT_ID,
            f"База данных очищена\n\nУдалено записей: {count}"
        )
    
    async def start(self):
        print("AI-МОЗГ ЗАПУЩЕН")
        print("Жду команд в Telegram...")
        
        await self.bot.send_message(
            CHAT_ID,
            "AI-МОЗГ ЗАПУЩЕН\n\nПриступай к работе! Используй /start для просмотра команд."
        )
        
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        await self.bot.session.close()
        self.db.close()
        print("AI-МОЗГ ОСТАНОВЛЕН")


def select_project_path():
    """Выбор пути к проекту при запуске"""
    print("\n" + "="*60)
    print("🧠 AI-МОЗГ - Выбор папки с сайтом")
    print("="*60)
    
    current_dir = os.getcwd()
    print(f"\n📍 Текущая директория: {current_dir}")
    
    # Ищем доступные папки с сайтами
    available_folders = []
    
    # Проверяем папку website
    website_dir = os.path.join(current_dir, 'website')
    if os.path.exists(website_dir):
        available_folders.append(('website', website_dir))
    
    # Проверяем текущую директорию
    if os.path.exists(os.path.join(current_dir, 'tests')):
        available_folders.append(('текущая директория', current_dir))
    
    print("\n📁 Доступные варианты:")
    print("1. 🌐 Папка website (рекомендуется)")
    print("2. 📂 Текущая директория")
    print("3. ✏️  Указать свой путь")
    
    choice = input("\n👉 Твой выбор (1-3): ").strip()
    
    if choice == "1":
        # Используем папку website
        project_path = website_dir
        if not os.path.exists(project_path):
            print(f"\n⚠️ Папка website не найдена, создаю...")
            os.makedirs(project_path, exist_ok=True)
        print(f"✓ Выбрано: {project_path}")
    
    elif choice == "2":
        # Используем текущую директорию
        project_path = current_dir
        print(f"✓ Выбрано: {project_path}")
    
    elif choice == "3":
        # Пользователь указывает свой путь
        custom_path = input("\n📝 Введи полный путь к папке с сайтом: ").strip()
        if os.path.exists(custom_path):
            project_path = custom_path
            print(f"✓ Выбрано: {project_path}")
        else:
            print(f"⚠️ Путь не существует: {custom_path}")
            print("Использую текущую директорию")
            project_path = current_dir
    
    else:
        print("⚠️ Неверный выбор, использую папку website")
        project_path = website_dir
        if not os.path.exists(project_path):
            os.makedirs(project_path, exist_ok=True)
    
    # Проверяем наличие папки tests
    tests_path = os.path.join(project_path, 'tests')
    if not os.path.exists(tests_path):
        print(f"\n⚠️ Папка 'tests' не найдена в {project_path}")
        print("📁 Создаю папку 'tests'...")
        os.makedirs(tests_path, exist_ok=True)
        print(f"✓ Создана папка: {tests_path}")
    else:
        print(f"✓ Найдена папка tests: {tests_path}")
    
    print("\n" + "="*60)
    return project_path


async def main():
    # Выбор проекта при запуске
    project_path = select_project_path()
    
    brain = AIBrain(project_path=project_path)
    try:
        await brain.start()
    except KeyboardInterrupt:
        await brain.stop()


if __name__ == "__main__":
    asyncio.run(main())
