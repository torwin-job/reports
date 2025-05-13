#!/usr/bin/env python3
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Type, Optional


class ReportFormatter(ABC):
    """
    Абстрактный базовый класс для форматеров отчетов.
    """
    
    @abstractmethod
    def format(self, data: Dict[str, Any]) -> str:
        """
        Форматирует данные отчета в строку.
        
        Args:
            data: Данные отчета
            
        Returns:
            Строка с отформатированным отчетом
        """
        pass


class TextFormatter(ReportFormatter):
    """
    Форматер для текстового представления отчета.
    """
    
    def format(self, data: Dict[str, Any]) -> str:
        """
        Форматирует данные отчета в текстовый формат.
        
        Args:
            data: Данные отчета с ключами 'items' и 'total'
            
        Returns:
            Строка с текстовым представлением отчета
        """
        if not data or 'items' not in data or 'total' not in data:
            return "Нет данных для форматирования"
        
        report = []
        report.append("-" * 80)
        report.append(f"{'Имя':30} | {'Отдел':20} | {'Часы':10} | {'Ставка':10} | {'Сумма':10}")
        report.append("-" * 80)
        
        for item in data['items']:
            name = item.get('name', '')
            department = item.get('department', '')
            hours = item.get('hours', 0)
            rate = item.get('rate', 0)
            amount = item.get('amount', 0)
            
            report.append(f"{name:30} | {department:20} | {hours:10.1f} | {rate:10.2f} | {amount:10.2f}")
        
        report.append("-" * 80)
        report.append(f"{'Итого':74} | {data['total']:10.2f}")
        report.append("-" * 80)
        
        return "\n".join(report)


class JsonFormatter(ReportFormatter):
    """
    Форматер для JSON представления отчета.
    """
    
    def format(self, data: Dict[str, Any]) -> str:
        """
        Форматирует данные отчета в JSON.
        
        Args:
            data: Данные отчета
            
        Returns:
            Строка с JSON представлением отчета
        """
        return json.dumps(data, ensure_ascii=False, indent=2)


class FormatterFactory:
    """
    Фабрика для создания форматеров отчетов.
    """
    
    _formatters: Dict[str, Type[ReportFormatter]] = {
        'text': TextFormatter,
        'json': JsonFormatter,
    }
    
    @classmethod
    def register_formatter(cls, format_type: str, formatter_class: Type[ReportFormatter]) -> None:
        """
        Регистрирует новый тип форматера отчетов.
        
        Args:
            format_type: Название типа форматера
            formatter_class: Класс форматера отчетов
        """
        cls._formatters[format_type] = formatter_class
    
    @classmethod
    def get_formatter(cls, format_type: str) -> Optional[ReportFormatter]:
        """
        Возвращает форматер отчетов для заданного типа.
        
        Args:
            format_type: Тип форматера
            
        Returns:
            Экземпляр форматера отчетов или None, если тип не поддерживается
        """
        formatter_class = cls._formatters.get(format_type)
        
        if formatter_class:
            return formatter_class()
        
        return None 