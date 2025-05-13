#!/usr/bin/env python3
import pytest
from typing import List, Dict, Any

from src.reports.report_generator import ReportFactory, PayoutReportGenerator, ReportGenerator


@pytest.fixture
def sample_employees_data():
    """
    Фикстура, создающая тестовые данные сотрудников.
    """
    return [
        {
            'id': '1',
            'email': 'alice@example.com',
            'name': 'Alice Johnson',
            'department': 'Marketing',
            'hours_worked': '160',
            'hourly_rate': '50'
        },
        {
            'id': '2',
            'email': 'bob@example.com',
            'name': 'Bob Smith',
            'department': 'Design',
            'hours_worked': '150',
            'hourly_rate': '40'
        },
        {
            'id': '3',
            'email': 'carol@example.com',
            'name': 'Carol Williams',
            'department': 'Design',
            'hours_worked': '170',
            'hourly_rate': '60'
        }
    ]


@pytest.fixture
def sample_employees_data_different_rate_keys():
    """
    Фикстура, создающая тестовые данные сотрудников с разными ключами для ставки.
    """
    return [
        {
            'id': '1',
            'email': 'alice@example.com',
            'name': 'Alice Johnson',
            'department': 'Marketing',
            'hours_worked': '160',
            'hourly_rate': '50'
        },
        {
            'id': '2',
            'email': 'bob@example.com',
            'name': 'Bob Smith',
            'department': 'Design',
            'hours_worked': '150',
            'rate': '40'
        },
        {
            'id': '3',
            'email': 'carol@example.com',
            'name': 'Carol Williams',
            'department': 'Design',
            'hours_worked': '170',
            'salary': '60'
        }
    ]


def test_payout_report_generator(sample_employees_data):
    """
    Тест генератора отчетов по заработной плате.
    """
    generator = PayoutReportGenerator()
    report_data = generator.generate(sample_employees_data)
    
    assert isinstance(report_data, dict)
    assert report_data['report_type'] == 'payout'
    assert 'items' in report_data
    assert 'total' in report_data
    
    assert len(report_data['items']) == 3
    
    # Проверка данных сотрудников
    assert report_data['items'][0]['name'] == 'Alice Johnson'
    assert report_data['items'][0]['department'] == 'Marketing'
    assert report_data['items'][0]['hours'] == 160.0
    assert report_data['items'][0]['rate'] == 50.0
    assert report_data['items'][0]['amount'] == 8000.0
    
    assert report_data['items'][1]['name'] == 'Bob Smith'
    assert report_data['items'][1]['department'] == 'Design'
    assert report_data['items'][1]['hours'] == 150.0
    assert report_data['items'][1]['rate'] == 40.0
    assert report_data['items'][1]['amount'] == 6000.0
    
    assert report_data['items'][2]['name'] == 'Carol Williams'
    assert report_data['items'][2]['department'] == 'Design'
    assert report_data['items'][2]['hours'] == 170.0
    assert report_data['items'][2]['rate'] == 60.0
    assert report_data['items'][2]['amount'] == 10200.0
    
    # Проверка итоговой суммы
    assert report_data['total'] == 24200.0


def test_payout_report_generator_different_rate_keys(sample_employees_data_different_rate_keys):
    """
    Тест генератора отчетов с разными ключами для ставки.
    """
    generator = PayoutReportGenerator()
    report_data = generator.generate(sample_employees_data_different_rate_keys)
    
    # Проверка расчета суммы с разными ключами ставки
    assert report_data['items'][0]['amount'] == 8000.0  # 160 * 50 (hourly_rate)
    assert report_data['items'][1]['amount'] == 6000.0  # 150 * 40 (rate)
    assert report_data['items'][2]['amount'] == 10200.0  # 170 * 60 (salary)
    
    # Проверка итоговой суммы
    assert report_data['total'] == 24200.0


def test_report_factory_get_generator():
    """
    Тест получения генератора отчетов через фабрику.
    """
    # Проверка получения существующего генератора
    generator = ReportFactory.get_generator('payout')
    assert isinstance(generator, PayoutReportGenerator)
    
    # Проверка получения несуществующего генератора
    generator = ReportFactory.get_generator('nonexistent')
    assert generator is None


def test_report_factory_register_generator():
    """
    Тест регистрации нового генератора отчетов.
    """
    # Создаем тестовый класс генератора отчетов
    class TestReportGenerator(ReportGenerator):
        def generate(self, employees_data: List[Dict[str, Any]]) -> Dict[str, Any]:
            return {"report_type": "test", "items": [], "total": 0}
    
    # Регистрируем новый генератор
    ReportFactory.register_generator('test', TestReportGenerator)
    
    # Проверяем, что генератор зарегистрирован
    generator = ReportFactory.get_generator('test')
    assert isinstance(generator, TestReportGenerator)
    
    # Проверяем работу нового генератора
    report_data = generator.generate([])
    assert report_data == {"report_type": "test", "items": [], "total": 0} 