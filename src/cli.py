import argparse

def parse_arguments():
    """Получаем аргументы для cli из командной строки"""
    parser = argparse.ArgumentParser(description="Обработчик лог файлов")
    parser.add_argument(
        "--file",
        nargs="+",
        required=True,
        help="Путь к лог файлам")
    parser.add_argument(
        "--report",
        choices=["average"],
        required=True,
        help="Тип отчета")
    parser.add_argument(
        "--date",
        help="Фильтр по дате в формате год день месяц (ГГГГ-ДД-ММ)")

    return parser.parse_args()