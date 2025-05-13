#!/usr/bin/env python3
import argparse
import sys
from typing import List, Dict, Any
import os

from src.utils.csv_reader import CSVReader
from src.reports.report_generator import ReportFactory
from src.reports.formatters import FormatterFactory


def validate_files(file_paths: List[str]) -> List[str]:
    """
    Проверяет существование файлов и их расширение.
    
    Args:
        file_paths: Список путей к файлам
        
    Returns:
        Список корректных путей к файлам
    """
    valid_paths = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Предупреждение: Файл {file_path} не существует и будет пропущен")
            continue
            
        if not file_path.lower().endswith('.csv'):
            print(f"Предупреждение: Файл {file_path} не имеет расширения CSV и будет пропущен")
            continue
            
        valid_paths.append(file_path)
    
    return valid_paths


def validate_report_type(report_type: str) -> bool:
    """
    Проверяет корректность типа отчета.
    
    Args:
        report_type: Тип отчета
        
    Returns:
        True если тип отчета поддерживается, иначе False
    """
    return report_type in ['payout']


def validate_format_type(format_type: str) -> bool:
    """
    Проверяет корректность типа формата.
    
    Args:
        format_type: Тип формата вывода
        
    Returns:
        True если тип формата поддерживается, иначе False
    """
    return format_type in ['json', 'text']


def save_to_file(content: str, output_file: str) -> bool:
    """
    Сохраняет содержимое в файл.
    
    Args:
        content: Содержимое для сохранения
        output_file: Путь к файлу для сохранения
        
    Returns:
        True если сохранение успешно, иначе False
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении в файл {output_file}: {str(e)}")
        return False


def main():
    """
    Основная функция программы
    """
    parser = argparse.ArgumentParser(description='Генератор отчетов по данным сотрудников')
    parser.add_argument('files', nargs='+', help='CSV файлы с данными сотрудников')
    parser.add_argument('--report', required=True, help='Тип отчета (например, payout)')
    parser.add_argument('--format', default='json', help='Формат вывода (json или text)')
    parser.add_argument('--output', help='Путь к файлу для сохранения результата. Если не указан, результат выводится в консоль')
    
    try:
        args = parser.parse_args()
    except Exception as e:
        print(f"Ошибка при разборе аргументов: {str(e)}")
        parser.print_help()
        sys.exit(1)
    
    # Проверка корректности аргументов
    valid_files = validate_files(args.files)
    
    if not valid_files:
        print("Ошибка: Не указаны корректные CSV файлы")
        sys.exit(1)
    
    if not validate_report_type(args.report):
        print(f"Ошибка: Неподдерживаемый тип отчета '{args.report}'. Поддерживаемые типы: payout")
        sys.exit(1)
    
    if not validate_format_type(args.format):
        print(f"Ошибка: Неподдерживаемый формат вывода '{args.format}'. Поддерживаемые форматы: json, text")
        sys.exit(1)
    
    # Проверка выходного файла
    output_file = args.output
    if output_file and os.path.exists(output_file):
        overwrite = input(f"Файл {output_file} уже существует. Перезаписать? (y/n): ")
        if overwrite.lower() != 'y':
            print("Отмена операции")
            sys.exit(0)
    
    all_employees_data = []
    
    # Чтение данных из всех указанных файлов
    for file_path in valid_files:
        try:
            employees_data = CSVReader.read_file(file_path)
            all_employees_data.extend(employees_data)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {str(e)}")
    
    if not all_employees_data:
        print("Ошибка: Не удалось прочитать данные из указанных файлов")
        sys.exit(1)
    
    # Получение генератора отчетов
    report_generator = ReportFactory.get_generator(args.report)
    
    if not report_generator:
        print(f"Ошибка: Не удалось создать генератор отчета типа '{args.report}'")
        sys.exit(1)
    
    # Получение форматера отчетов
    formatter = FormatterFactory.get_formatter(args.format)
    
    if not formatter:
        print(f"Ошибка: Не удалось создать форматер типа '{args.format}'")
        sys.exit(1)
    
    try:
        # Генерация отчета
        report_data = report_generator.generate(all_employees_data)
        
        # Форматирование отчета
        formatted_report = formatter.format(report_data)
        
        # Сохранение или вывод результата
        if output_file:
            if save_to_file(formatted_report, output_file):
                print(f"Отчет успешно сохранен в файл: {output_file}")
            else:
                print(f"Не удалось сохранить отчет в файл: {output_file}")
                sys.exit(1)
        else:
            print(formatted_report)
    except Exception as e:
        print(f"Ошибка при генерации или форматировании отчета: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main() 