import json
from datetime import datetime
from collections import defaultdict
import sys


class LogAnalyzer:
    def __init__(self):
        self.records = []

    def read_and_safe_logs(self, files):
        """Читаем и сохраняем логи"""
        for file in files:
            try:
                with open(file, 'r') as f:
                    for line in f:
                        self.records.append(json.loads(line))
            # ошибка на случай если лог файл не найден
            except FileNotFoundError:
                print(f"Ошибка: Файл {file} не найден")
                sys.exit(1)
            # ошибка на случай если формат файла некорректный
            except json.JSONDecodeError:
                print(f"Ошибка: некорректный формат в файле {file}")
                sys.exit(1)

    def filter_by_date(self, target_date):
        """Фильтруем логи по дате"""
        try:
            target = datetime.strptime(target_date, "%Y-%d-%m").date()
            result = [record for record in self.records
                      if datetime.fromisoformat(record['@timestamp']).date() == target]
            return result
        # ошибка на случай неверного формата дата
        except ValueError:
            print("Ошибка: Неверный формат даты. Используйте ГГГГ-ДД-ММ")
            sys.exit(1)

    def generate_average_report(self, data=None):
        """Генерируем отчет по среднему времени ответа"""
        data = data or self.records
        endpoint_stats = defaultdict(lambda: {"total": 0, "sum_time": 0.0})

        for record in data:
            url = record["url"]
            response_time = record["response_time"]
            endpoint_stats[url]["total"] += 1
            endpoint_stats[url]["sum_time"] += response_time

        result = [(url, stats['total'], round(stats['sum_time'] / stats['total'], 3))
                  for url, stats in endpoint_stats.items()]
        sorted_result = sorted(result, key=lambda x: x[1], reverse=True)

        return sorted_result