import sys
import os

# Добавляем путь к основному скрипту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import get_book_data, scrape_books


def test_get_book_data_returns_dict():
    """Тест: функция возвращает словарь"""
    test_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    result = get_book_data(test_url)
    assert type(result) == dict


def test_get_book_data_has_book_name():
    """Тест: в данных есть название книги"""
    test_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    result = get_book_data(test_url)
    assert "book_name" in result
    assert result["book_name"] != ""


def test_scrape_books_returns_list():
    """Тест: функция возвращает список"""
    result = scrape_books(is_save=False)
    assert type(result) == list
