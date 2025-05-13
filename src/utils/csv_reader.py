#!/usr/bin/env python3
import os
from typing import List, Dict, Any


class CSVReader:
    """
    Класс для чтения данных из CSV файлов.
    """
    
    @staticmethod
    def read_file(file_path: str) -> List[Dict[str, Any]]:
        """
        Читает CSV файл и возвращает список словарей с данными.
        
        Args:
            file_path: Путь к CSV файлу
            
        Returns:
            Список словарей с данными
        """
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл {file_path} не найден")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            if not lines:
                print(f"Предупреждение: Файл {file_path} пуст")
                return []
                
            header = lines[0].strip().split(',')
            data = []
            
            for line_num, line in enumerate(lines[1:], start=2):
                if line.strip():
                    values = line.strip().split(',')
                    if len(values) == len(header):
                        employee_data = {header[i]: values[i] for i in range(len(header))}
                        data.append(employee_data)
                    else:
                        print(f"Предупреждение: Некорректная строка {line_num} в файле {file_path}: {line.strip()}")
                        
            return data
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {str(e)}")
            return [] 