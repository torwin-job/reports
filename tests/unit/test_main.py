#!/usr/bin/env python3
import os
import tempfile
import pytest

from main import validate_files, validate_report_type, validate_format_type, save_to_file


def test_validate_files(tmpdir):
    """
    Тест функции валидации файлов.
    """
    # Создаем временные файлы
    csv_file = tmpdir.join("test.csv")
    csv_file.write("test")
    
    txt_file = tmpdir.join("test.txt")
    txt_file.write("test")
    
    nonexistent_file = str(tmpdir.join("nonexistent.csv"))
    
    # Тестируем валидацию
    result = validate_files([str(csv_file), str(txt_file), nonexistent_file])
    
    assert len(result) == 1
    assert str(csv_file) in result
    assert str(txt_file) not in result
    assert nonexistent_file not in result


def test_validate_report_type():
    """
    Тест функции валидации типа отчета.
    """
    assert validate_report_type('payout') is True
    assert validate_report_type('nonexistent') is False


def test_validate_format_type():
    """
    Тест функции валидации типа формата.
    """
    assert validate_format_type('json') is True
    assert validate_format_type('text') is True
    assert validate_format_type('nonexistent') is False


def test_save_to_file():
    """
    Тест функции сохранения в файл.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    try:
        content = "Test content"
        
        # Проверка успешного сохранения
        assert save_to_file(content, temp_file_path) is True
        
        # Проверка содержимого файла
        with open(temp_file_path, 'r', encoding='utf-8') as file:
            saved_content = file.read()
            assert saved_content == content
        
        # Проверка неудачного сохранения (неверный путь)
        invalid_path = "/nonexistent/directory/file.txt"
        assert save_to_file(content, invalid_path) is False
    finally:
        # Очистка
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path) 