import pytest
from src.log_handler import LogHandler
from datetime import datetime
import json
import os


@pytest.fixture
def sample_handler():
    handler = LogHandler()
    handler.records = [
        {"@timestamp": "2025-06-22T10:00:00+00:00", "url": "/api/test1", "response_time": 0.1},
        {"@timestamp": "2025-06-22T11:00:00+00:00", "url": "/api/test2", "response_time": 0.2},
        {"@timestamp": "2025-06-23T10:00:00+00:00", "url": "/api/test1", "response_time": 0.3}
    ]
    return handler


@pytest.fixture
def temp_log_file(tmp_path):
    """Временный файл для тестирования"""
    file_path = tmp_path / "test.log"
    data = [
        {"@timestamp": "2025-06-22T10:00:00+00:00", "url": "/api/temp", "response_time": 0.5},
        {"@timestamp": "2025-06-22T11:00:00+00:00", "url": "/api/temp", "response_time": 0.7}
    ]
    with open(file_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')
    return file_path


# Тесты для filter_by_date
def test_filter_by_date_correct(sample_handler):
    """Тест для корректной даты"""
    filtered = sample_handler.filter_by_date("2025-22-06")
    assert len(filtered) == 2
    assert all(datetime.fromisoformat(r["@timestamp"]).date().day == 22
               for r in filtered)


def test_filter_by_date_no_matches(sample_handler):
    """Тест для несуществующей в файле даты"""
    filtered = sample_handler.filter_by_date("2024-01-01")
    assert len(filtered) == 0


def test_filter_by_date_wrong_format(sample_handler, capsys):
    """Тест для неверного формата даты"""
    with pytest.raises(SystemExit):
        sample_handler.filter_by_date("2025/22/06")
    captured = capsys.readouterr()
    assert "Неверный формат даты" in captured.out


# Тесты для generate_average_report
def test_generate_report_basic(sample_handler):
    """Тест для всех данных"""
    report = sample_handler.generate_average_report()
    assert len(report) == 2
    assert ("/api/test1", 2, 0.2) in report
    assert ("/api/test2", 1, 0.2) in report


def test_generate_report_filtered(sample_handler):
    """Тест для отфильтрованных данных"""
    filtered = sample_handler.filter_by_date("2025-22-06")
    report = sample_handler.generate_average_report(filtered)
    assert len(report) == 2
    assert ("/api/test1", 1, 0.1) in report
    assert ("/api/test2", 1, 0.2) in report

# Тесты для read_and_safe_logs
def test_read_and_safe_logs_valid_file(temp_log_file):
    """Тест чтения корректного лог-файла"""
    handler = LogHandler()
    handler.read_and_safe_logs([temp_log_file])
    assert len(handler.records) == 2
    assert handler.records[0]["url"] == "/api/temp"


def test_read_and_safe_logs_file_not_found(capsys):
    """Тест если файл отсутствует"""
    handler = LogHandler()
    with pytest.raises(SystemExit):
        handler.read_and_safe_logs(["nonexistent.log"])
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_read_and_safe_logs_invalid_json(tmp_path, capsys):
    """Тест для некорректного JSON файла"""
    file_path = tmp_path / "invalid.log"
    with open(file_path, 'w') as f:
        f.write('{"invalid": "json"\n')

    handler = LogHandler()
    with pytest.raises(SystemExit):
        handler.read_and_safe_logs([file_path])
    captured = capsys.readouterr()
    assert "некорректный формат" in captured.out
