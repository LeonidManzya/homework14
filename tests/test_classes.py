import pytest

from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_counters():
    Category.total_categories = 0
    Category.total_products = 0
    yield
    Category.total_categories = 0
    Category.total_products = 0


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
    assert Category.total_categories == 1
    assert Category.total_products == 2


def test_multiple_categories_with_products_counter():
    products1 = [
        Product("Телефон", "Смартфон", 50000, 10),
        Product("Ноутбук", "Игровой ноутбук", 100000, 5),
    ]
    products2 = [Product("Роман", "Художественная литература", 500, 20)]

    category1 = Category("Электроника", "Техника и гаджеты", products1)
    category2 = Category("Книги", "Художественная литература", products2)

    assert Category.total_categories == 2
    assert Category.total_products == 3


def test_category_creation_empty_products():
    category = Category("Электроника", "Техника и гаджеты")

    assert category.name == "Электроника"
    assert category.description == "Техника и гаджеты"
    assert category.products == []
    assert Category.total_categories == 1
    assert Category.total_products == 0


def test_product_in_category():
    product = Product("Телефон", "Смартфон", 50000, 10)
    category = Category("Электроника", "Техника и гаджеты", [product])

    assert len(category.products) == 1
    assert category.products[0].name == "Телефон"
    assert category.products[0].price == 50000
    assert category.products[0].quantity == 10
