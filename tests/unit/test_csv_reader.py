#!/usr/bin/env python3
import os
import pytest
import tempfile
from typing import List, Dict, Any

from src.utils.csv_reader import CSVReader


@pytest.fixture
def sample_csv_file():
    """
    Фикстура, создающая временный CSV файл с тестовыми данными.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file.write("id,email,name,department,hours_worked,hourly_rate\n")
        temp_file.write("1,alice@example.com,Alice Johnson,Marketing,160,50\n")
        temp_file.write("2,bob@example.com,Bob Smith,Design,150,40\n")
        temp_file.write("3,carol@example.com,Carol Williams,Design,170,60\n")
        temp_file_path = temp_file.name
    
    yield temp_file_path
    
    # Удаляем временный файл после использования
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)


@pytest.fixture
def empty_csv_file():
    """
    Фикстура, создающая пустой CSV файл.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file_path = temp_file.name
    
    yield temp_file_path
    
    # Удаляем временный файл после использования
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)


def test_read_file_success(sample_csv_file):
    """
    Тест успешного чтения CSV файла.
    """
    result = CSVReader.read_file(sample_csv_file)
    
    assert len(result) == 3
    assert result[0]['name'] == 'Alice Johnson'
    assert result[1]['department'] == 'Design'
    assert result[2]['hours_worked'] == '170'
    assert result[2]['hourly_rate'] == '60'


def test_read_file_nonexistent():
    """
    Тест чтения несуществующего файла.
    """
    result = CSVReader.read_file("nonexistent_file.csv")
    
    assert result == []


def test_read_empty_file(empty_csv_file):
    """
    Тест чтения пустого файла.
    """
    result = CSVReader.read_file(empty_csv_file)
    
    assert result == []


def test_read_file_with_different_rate_column():
    """
    Тест чтения файла с разными названиями колонки ставки.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file.write("id,email,name,department,hours_worked,rate\n")
        temp_file.write("1,alice@example.com,Alice Johnson,Marketing,160,50\n")
        temp_file_path = temp_file.name
    
    try:
        result = CSVReader.read_file(temp_file_path)
        
        assert len(result) == 1
        assert result[0]['rate'] == '50'
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file.write("id,email,name,department,hours_worked,salary\n")
        temp_file.write("1,alice@example.com,Alice Johnson,Marketing,160,50\n")
        temp_file_path = temp_file.name
    
    try:
        result = CSVReader.read_file(temp_file_path)
        
        assert len(result) == 1
        assert result[0]['salary'] == '50'
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path) 