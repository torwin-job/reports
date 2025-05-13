#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type


class ReportGenerator(ABC):
    """
    Абстрактный базовый класс для генераторов отчетов.
    """
    
    @abstractmethod
    def generate(self, employees_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Генерирует отчет на основе данных сотрудников.
        
        Args:
            employees_data: Список словарей с данными сотрудников
            
        Returns:
            Словарь с данными отчета
        """
        pass


class PayoutReportGenerator(ReportGenerator):
    """
    Генератор отчетов по заработной плате.
    """
    
    def generate(self, employees_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Генерирует отчет по заработной плате.
        
        Args:
            employees_data: Список словарей с данными сотрудников
            
        Returns:
            Словарь с данными отчета
        """
        items = []
        total_payout = 0
        
        for employee in employees_data:
            name = employee.get('name', '')
            department = employee.get('department', '')
            
            try:
                hours_worked = float(employee.get('hours_worked', 0))
                
                # Проверяем разные возможные названия колонки со ставкой
                rate = 0
                for rate_key in ['hourly_rate', 'rate', 'salary']:
                    if rate_key in employee:
                        rate = float(employee[rate_key])
                        break
                
                amount = hours_worked * rate
                total_payout += amount
                
                employee_item = {
                    'name': name,
                    'department': department,
                    'hours': hours_worked,
                    'rate': rate,
                    'amount': amount
                }
                
                items.append(employee_item)
            except (ValueError, TypeError) as e:
                print(f"Ошибка обработки данных для {name}: {str(e)}")
        
        return {
            'report_type': 'payout',
            'items': items,
            'total': total_payout
        }


class ReportFactory:
    """
    Фабрика для создания генераторов отчетов.
    """
    
    _generators: Dict[str, Type[ReportGenerator]] = {
        'payout': PayoutReportGenerator,
    }
    
    @classmethod
    def register_generator(cls, report_type: str, generator_class: Type[ReportGenerator]) -> None:
        """
        Регистрирует новый тип генератора отчетов.
        
        Args:
            report_type: Название типа отчета
            generator_class: Класс генератора отчетов
        """
        cls._generators[report_type] = generator_class
    
    @classmethod
    def get_generator(cls, report_type: str) -> Optional[ReportGenerator]:
        """
        Возвращает генератор отчетов для заданного типа.
        
        Args:
            report_type: Тип отчета
            
        Returns:
            Экземпляр генератора отчетов или None, если тип не поддерживается
        """
        generator_class = cls._generators.get(report_type)
        
        if generator_class:
            return generator_class()
        
        return None 