#!/usr/bin/env python3
import json
import pytest
from typing import Dict, Any

from src.reports.formatters import FormatterFactory, JsonFormatter, ReportFormatter, TextFormatter


@pytest.fixture
def sample_report_data() -> Dict[str, Any]:
    """
    Фикстура, создающая тестовые данные отчета.
    """
    return {
        'report_type': 'payout',
        'items': [
            {
                'name': 'Alice Johnson',
                'department': 'Marketing',
                'hours': 160.0,
                'rate': 50.0,
                'amount': 8000.0
            },
            {
                'name': 'Bob Smith',
                'department': 'Design',
                'hours': 150.0,
                'rate': 40.0,
                'amount': 6000.0
            },
            {
                'name': 'Carol Williams',
                'department': 'Design',
                'hours': 170.0,
                'rate': 60.0,
                'amount': 10200.0
            }
        ],
        'total': 24200.0
    }


def test_json_formatter(sample_report_data):
    """
    Тест JSON форматера.
    """
    formatter = JsonFormatter()
    result = formatter.format(sample_report_data)
    
    assert isinstance(result, str)
    
    # Проверяем, что результат можно распарсить обратно в JSON
    parsed_data = json.loads(result)
    
    assert parsed_data['report_type'] == 'payout'
    assert len(parsed_data['items']) == 3
    assert parsed_data['items'][0]['name'] == 'Alice Johnson'
    assert parsed_data['items'][1]['department'] == 'Design'
    assert parsed_data['items'][2]['amount'] == 10200.0
    assert parsed_data['total'] == 24200.0


def test_formatter_factory_get_formatter():
    """
    Тест получения форматера через фабрику.
    """
    # Проверка получения JSON форматера
    formatter = FormatterFactory.get_formatter('json')
    assert isinstance(formatter, JsonFormatter)
    
    # Проверка получения несуществующего форматера
    formatter = FormatterFactory.get_formatter('nonexistent')
    assert formatter is None


def test_formatter_factory_register_formatter():
    """
    Тест регистрации нового форматера.
    """
    # Создаем тестовый класс форматера
    class TestFormatter(ReportFormatter):
        def format(self, data: Dict[str, Any]) -> str:
            return "Test format"
    
    # Регистрируем новый форматер
    FormatterFactory.register_formatter('test', TestFormatter)
    
    # Проверяем, что форматер зарегистрирован
    formatter = FormatterFactory.get_formatter('test')
    assert isinstance(formatter, TestFormatter)
    
    # Проверяем работу нового форматера
    result = formatter.format({})
    assert result == "Test format"


def test_text_formatter(sample_report_data):
    """
    Тест текстового форматера.
    """
    formatter = TextFormatter()
    result = formatter.format(sample_report_data)
    
    assert isinstance(result, str)
    
    # Проверяем наличие заголовков таблицы
    assert "Имя" in result
    assert "Отдел" in result
    assert "Часы" in result
    assert "Ставка" in result
    assert "Сумма" in result
    
    # Проверяем наличие данных сотрудников
    assert "Alice Johnson" in result
    assert "Marketing" in result
    assert "Bob Smith" in result
    assert "Design" in result
    assert "Carol Williams" in result
    
    # Проверяем наличие итоговой суммы
    assert "Итого" in result
    assert "24200.00" in result 