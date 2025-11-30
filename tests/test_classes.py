import pytest
import unittest

from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_creation():
    product = Product("Телефон", "Смартфон", 50000, 10)

    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 50000
    assert product.quantity == 10


def test_category_creation_with_products():
    products = [
        Product("Телефон", "Смартфон", 50000, 10),
        Product("Ноутбук", "Игровой ноутбук", 100000, 5),
    ]

    category = Category("Электроника", "Техника и гаджеты", products)

    assert category.name == "Электроника"
    assert category.description == "Техника и гаджеты"
    assert len(category.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_multiple_categories_with_products_counter():
    products1 = [
        Product("Телефон", "Смартфон", 50000, 10),
        Product("Ноутбук", "Игровой ноутбук", 100000, 5),
    ]
    products2 = [Product("Роман", "Художественная литература", 500, 20)]

    category1 = Category("Электроника", "Техника и гаджеты", products1)
    category2 = Category("Книги", "Художественная литература", products2)

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_category_creation_empty_products():
    category = Category("Электроника", "Техника и гаджеты")

    assert category.name == "Электроника"
    assert category.description == "Техника и гаджеты"
    assert category.products == []
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_product_in_category():
    product = Product("Телефон", "Смартфон", 50000, 10)
    category = Category("Электроника", "Техника и гаджеты", [product])

    assert len(category.products) == 1
    assert "Телефон" in category.products[0]
    assert "50000" in category.products[0]
    assert "10" in category.products[0]


def test_add_product_to_empty_category():
    category = Category("Электроника", "Техника")
    product = Product("Телефон", "Смартфон", 50000, 10)

    category.add_product(product)

    assert len(category.products) == 1
    assert "Телефон" in category.products[0]
    assert "50000" in category.products[0]


def test_add_product_updates_counter():
    category = Category("Электроника", "Техника")
    product = Product("Телефон", "Смартфон", 50000, 10)

    initial_count = Category.product_count

    category.add_product(product)

    assert Category.product_count == initial_count + 1


def test_products_getter_empty_category():
    category = Category("Электроника", "Техника")

    assert category.products == []


def test_products_getter_with_products():
    product1 = Product("Телефон", "Смартфон", 50000, 10)
    product2 = Product("Ноутбук", "Игровой", 100000, 5)
    category = Category("Электроника", "Техника", [product1, product2])

    products_info = category.products

    assert len(products_info) == 2
    assert products_info[0] == "Телефон, 50000 руб. Остаток: 10 шт."
    assert products_info[1] == "Ноутбук, 100000 руб. Остаток: 5 шт."


def test_new_product_creation():
    product_data = {
        'name': 'Телефон',
        'description': 'Смартфон',
        'price': 50000,
        'quantity': 10
    }

    product = Product.new_product(product_data)

    assert product.name == 'Телефон'
    assert product.description == 'Смартфон'
    assert product.price == 50000
    assert product.quantity == 10


def test_price_getter():
    product = Product("Телефон", "Смартфон", 50000, 10)

    assert product.price == 50000


def test_price_setter_valid():
    product = Product("Телефон", "Смартфон", 50000, 10)

    product.price = 45000

    assert product.price == 45000


def test_price_setter_invalid_negative(capsys):
    product = Product("Телефон", "Смартфон", 50000, 10)

    product.price = -100

    assert product.price == 50000
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_invalid_zero(capsys):
    product = Product("Телефон", "Смартфон", 50000, 10)

    product.price = 0

    assert product.price == 50000
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

def test_product_str():
    product = Product("Телефон", "Смартфон", 50000, 10)
    assert str(product) == "Телефон, 50000 руб. Остаток: 10 шт."


def test_product_add():
    product1 = Product("Товар A", "Описание A", 100, 10)
    product2 = Product("Товар B", "Описание B", 200, 2)
    assert product1 + product2 == 1400
