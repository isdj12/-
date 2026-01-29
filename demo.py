"""
Демонстрация работы без Telegram
"""
from core import ReportParser, ErrorAnalyzer, TestDatabase


def demo_analysis():
    print("=" * 60)
    print("  ДЕМОНСТРАЦИЯ АНАЛИЗА ТЕСТОВ")
    print("=" * 60)
    print()
    
    report_path = "test_reports/report.json"
    results = ReportParser.parse_pytest_json(report_path)
    db = TestDatabase()
    
    print(f"Найдено тестов: {len(results)}")
    print()
    
    passed = failed = 0
    
    for test in results:
        if test['status'] == 'PASSED':
            passed += 1
            print(f"[OK] {test['name']}")
        else:
            failed += 1
            print(f"\n{'='*60}")
            print(f"[FAIL] УПАЛ: {test['name']}")
            print(f"{'='*60}")
            
            error_info = ErrorAnalyzer.analyze_error(test['error_message'])
            
            if error_info:
                print(f"\nДиагноз: {error_info['diagnosis']}")
                print(f"\nРекомендации:")
                for i, rec in enumerate(error_info['recommendations'], 1):
                    print(f"   {i}. {rec}")
                
                db.add_test_result(
                    test['name'],
                    test['status'],
                    test['error_message'],
                    error_info['type']
                )
                
                failure_count = db.get_test_failure_count(test['name'])
                severity = ErrorAnalyzer.get_severity(failure_count)
                
                print(f"\n{severity}")
                if failure_count > 1:
                    print(f"[!] Тест падал {failure_count} раз за последние 7 дней")
    
    print(f"\n{'='*60}")
    print(f"  ИТОГО")
    print(f"{'='*60}")
    print(f"[OK] Успешно: {passed}")
    print(f"[FAIL] Упало: {failed}")
    print(f"Всего: {len(results)}")
    print()
    
    print(f"{'='*60}")
    print(f"  ТОП ПРОБЛЕМНЫХ ТЕСТОВ")
    print(f"{'='*60}")
    top_tests = db.get_top_failing_tests()
    if top_tests:
        for i, (test_name, count) in enumerate(top_tests, 1):
            print(f"{i}. {test_name}")
            print(f"   Падений: {count}")
    else:
        print("Нет данных")
    
    db.close()
    print()
    print("=" * 60)
    print("  АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)


if __name__ == "__main__":
    demo_analysis()
