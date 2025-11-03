import time
import requests
import schedule
from bs4 import BeautifulSoup
import re
from datetime import datetime


def get_book_data(book_url: str) -> dict:
    """
    Этот код парсит информацию с сайта книг.
    На вход подаем html ссылку в формает строки.
    book_name возвращает название книги в str, используя поиск по тэгу h1;
    book_price возвращает цену книги В ФУНТАХ в float;
    book_rank возвращает ранг книги - кол-во звездочек;
    book_count возвращает кол-во книг в наличии в int, используя поиск по нужному классу;
    book_info возвращает описание книги в str;
    cleaned_book_add возвращает в иде словаря информацию из таблицы КАК ОНА ЕСТЬ.
    """

    response = requests.get(book_url)  # используем get-запрос
    soup = BeautifulSoup(response.content, "html.parser")

    if response.status_code == 200:
        book_name = soup.find("h1").text.strip()
        book_price = float(soup.find(class_="price_color").text.strip()[1:])
        book_rank = soup.find(class_="star-rating")["class"][1]

        book_count_text = soup.find(class_="instock availability").text.strip()
        book_count = int("".join(re.findall(r"[1-9]", book_count_text)))

        book_info_element = soup.select_one("#product_description + p")
        book_info = (
            book_info_element.text.strip() if book_info_element else "No description"
        )

        table = soup.select_one(".table.table-striped")
        book_add = [row.text.strip() for row in table.find_all("tr")] if table else []
        cleaned_book_add = {}
        for item in book_add:
            for key in [
                "UPC",
                "Product Type",
                "Price (excl.tax)",
                "Price (incl. tax)",
                "Tax",
                "Availability",
                "Number of reviews",
            ]:
                if item.startswith(key):
                    value = item[
                        len(key) :
                    ].strip()  # создаем значение, которое начинается там, где заканчивается ключ
                    cleaned_book_add[key] = value
                    break
        result = {
            "book_name": book_name,
            "book_price": book_price,
            "book_rank": book_rank,
            "book_count": book_count,
            "book_info": book_info,
            "cleaned_book_add": cleaned_book_add,
        }
    return result


def scrape_books(is_save: bool = False) -> list:
    """
    Парсит все 50 страниц из католога.
    Если is_save = True, то сохраняем информацию о книгах в виде books_data.txt.
    """

    res = []

    for page in range(1, 51):
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        print(f"Страница {page}")

        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        for book in soup.select("article.product_pod"):
            book_link = book.select_one("h3 a")["href"]
            book_url = f'http://books.toscrape.com/catalogue/{book_link.replace("../../../", "")}'

            book_data = get_book_data(book_url)
            res.append(book_data)

    if is_save:
        with open("books_data.txt", "w", encoding="utf-8") as file:
            for book in res:
                file.write(f"{book}\n")
    return res


def schedule_parsing_19():
    print("Запускаем автоматический парсинг!")

    books_data = scrape_books(is_save=True)

    print("Парсинг завершен!")


schedule.every().day.at("19:00").do(schedule_parsing_19)

while True:
    schedule.run_pending()
    time.sleep(60)


def test_get_book_data_returns_dict():
    test_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    result = get_book_data(test_url)
    assert type(result) == dict


def test_get_book_data_has_book_name():
    test_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    result = get_book_data(test_url)
    assert "book_name" in result
    assert result["book_name"] != ""


def test_scrape_books_returns_list():
    result = scrape_books(is_save=False)
    assert type(result) == list