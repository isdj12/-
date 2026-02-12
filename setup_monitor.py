"""
Настройка мониторинга - выбор папки с тестами
"""
import os
import json
from tkinter import Tk, filedialog


def select_folder_gui():
    """Выбор папки через графический интерфейс"""
    print("Открываю окно выбора папки...")
    
    # Создаем скрытое окно tkinter
    root = Tk()
    root.withdraw()  # Скрываем главное окно
    root.attributes('-topmost', True)  # Поверх всех окон
    
    # Открываем диалог выбора папки
    folder_path = filedialog.askdirectory(
        title="Выберите папку с тестами",
        initialdir=os.getcwd()
    )
    
    root.destroy()
    
    return folder_path


def select_folder_console():
    """Выбор папки через консоль"""
    print("\n" + "="*60)
    print("  НАСТРОЙКА МОНИТОРИНГА ТЕСТОВ")
    print("="*60)
    print()
    print("Введите путь к папке с тестами")
    print("(или нажмите Enter для текущей папки)")
    print()
    
    folder_path = input("Путь к папке: ").strip()
    
    # Если пусто - используем текущую папку
    if not folder_path:
        folder_path = os.getcwd()
    
    # Убираем кавычки если есть
    folder_path = folder_path.strip('"').strip("'")
    
    return folder_path


def validate_folder(folder_path):
    """Проверяет, что папка существует"""
    if not folder_path:
        return False, "Папка не выбрана"
    
    if not os.path.exists(folder_path):
        return False, f"Папка не существует: {folder_path}"
    
    if not os.path.isdir(folder_path):
        return False, f"Это не папка: {folder_path}"
    
    return True, "OK"


def save_config(folder_path):
    """Сохраняет настройки в config.json"""
    config = {
        'test_folder': folder_path,
        'reports_dir': os.path.join(folder_path, 'test_reports'),
        'report_file': 'report.json'
    }
    
    with open('monitor_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\nНастройки сохранены в monitor_config.json")
    return config


def load_config():
    """Загружает настройки из config.json"""
    try:
        with open('monitor_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def setup_monitoring():
    """Главная функция настройки"""
    print("\n" + "="*60)
    print("  НАСТРОЙКА МОНИТОРИНГА")
    print("="*60)
    print()
    print("Выберите способ выбора папки:")
    print("1. Графический интерфейс (окно выбора)")
    print("2. Ввод пути в консоли")
    print()
    
    choice = input("Ваш выбор (1 или 2): ").strip()
    
    # Выбор папки
    if choice == "1":
        folder_path = select_folder_gui()
    else:
        folder_path = select_folder_console()
    
    # Проверка папки
    is_valid, message = validate_folder(folder_path)
    
    if not is_valid:
        print(f"\n[ОШИБКА] {message}")
        return None
    
    # Показываем выбранную папку
    print(f"\n[OK] Выбрана папка: {folder_path}")
    
    # Создаем папку для отчетов если её нет
    reports_dir = os.path.join(folder_path, 'test_reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"[OK] Создана папка для отчетов: {reports_dir}")
    
    # Сохраняем конфигурацию
    config = save_config(folder_path)
    
    print("\n" + "="*60)
    print("  НАСТРОЙКА ЗАВЕРШЕНА")
    print("="*60)
    print()
    print("Теперь запусти мониторинг:")
    print("  python monitor.py")
    print()
    
    return config


if __name__ == "__main__":
    setup_monitoring()
