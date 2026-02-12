"""
Telegram бот для уведомлений
"""
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, CHAT_ID
from core import TestDatabase, ErrorAnalyzer


class TesterBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.db = TestDatabase()
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.dp.message(Command('start'))
        async def cmd_start(message: types.Message):
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Последний отчет")],
                    [KeyboardButton(text="Топ проблем")],
                    [KeyboardButton(text="Что проверить?")],
                    [KeyboardButton(text="Очистить БД")]
                ],
                resize_keyboard=True
            )
            await message.answer(
                "Привет! Я твой ассистент по тестированию.\n\n"
                "Я буду следить за тестами и сообщать о проблемах.",
                reply_markup=keyboard
            )
        
        @self.dp.message(lambda message: message.text == "Последний отчет")
        async def last_report(message: types.Message):
            summary = self.db.get_last_run_summary()
            if not summary:
                await message.answer("Нет данных за последние 24 часа")
                return
            
            text = "Отчет за последние 24 часа:\n\n"
            for status, count in summary:
                prefix = "[OK]" if status == "PASSED" else "[FAIL]"
                text += f"{prefix} {status}: {count}\n"
            
            await message.answer(text)
        
        @self.dp.message(lambda message: message.text == "Топ проблем")
        async def top_problems(message: types.Message):
            top_tests = self.db.get_top_failing_tests()
            if not top_tests:
                await message.answer("Нет проблемных тестов за последнюю неделю!")
                return
            
            text = "Топ падающих тестов (за 7 дней):\n\n"
            for i, (test_name, count) in enumerate(top_tests, 1):
                text += f"{i}. {test_name}\n   Падений: {count}\n\n"
            
            await message.answer(text)
        
        @self.dp.message(lambda message: message.text == "Что проверить?")
        async def recommendations(message: types.Message):
            await message.answer(
                "Общие рекомендации:\n\n"
                "1. Проверь статус всех сервисов\n"
                "2. Убедись, что тестовые данные актуальны\n"
                "3. Проверь логи за последний час\n"
                "4. Убедись, что нет проблем с сетью"
            )
        
        @self.dp.message(lambda message: message.text == "Очистить БД")
        async def clear_database(message: types.Message):
            try:
                # Получаем количество записей до очистки
                cursor = self.db.conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM test_runs')
                count_before = cursor.fetchone()[0]
                
                # Очищаем базу данных
                cursor.execute('DELETE FROM test_runs')
                self.db.conn.commit()
                
                await message.answer(
                    f"База данных очищена!\n\n"
                    f"Удалено записей: {count_before}\n\n"
                    f"Теперь можешь запускать новые тесты."
                )
            except Exception as e:
                await message.answer(f"Ошибка при очистке БД: {e}")
    
    async def send_test_notification(self, test_name, status, error_info=None, failure_count=0):
        if status == "PASSED":
            message = f"[OK] Тест прошел успешно\n\n{test_name}"
        else:
            severity = ErrorAnalyzer.get_severity(failure_count)
            message = f"{severity}\n\n"
            message += f"[FAIL] Упал тест: {test_name}\n\n"
            
            if error_info:
                message += f"Диагноз: {error_info['diagnosis']}\n\n"
                message += "Что проверить:\n"
                for i, rec in enumerate(error_info['recommendations'], 1):
                    message += f"{i}. {rec}\n"
                
                if failure_count > 1:
                    message += f"\n[!] Тест падал {failure_count} раз за последние 7 дней"
        
        await self.bot.send_message(CHAT_ID, message)
    
    async def start_polling(self):
        await self.dp.start_polling(self.bot)
    
    async def close(self):
        await self.bot.session.close()
        self.db.close()
