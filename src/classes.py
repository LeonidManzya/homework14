from abc import ABC, abstractmethod


class Mixin:
    def __init__(self, *args, **kwargs):
        self._init_args = args
        self._init_kwargs = kwargs

        class_name = self.__class__.__name__
        print(f"Создан объект класса {class_name} с параметрами:")

        if args:
            print(f"  Позиционные аргументы: {args}")

        if kwargs:
            print(f"  Именованные аргументы: {kwargs}")

        if not args and not kwargs:
            print("  (без аргументов)")

        print()

        super().__init__(*args, **kwargs)

    def __repr__(self):
        class_name = self.__class__.__name__
        args_str = ", ".join([repr(arg) for arg in self._init_args])
        kwargs_str = ", ".join([f"{k}={repr(v)}" for k, v in self._init_kwargs.items()])

        all_args = []
        if args_str:
            all_args.append(args_str)
        if kwargs_str:
            all_args.append(kwargs_str)

        return f"{class_name}({', '.join(all_args)})"


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass


class Product(Mixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        super().__init__(name, description, price, quantity)
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        if type(self) != type(other):
            raise TypeError("Можно складывать только товары из одинаковых классов продуктов")

        total_self = self.price * self.quantity
        total_other = other.price * other.quantity
        return total_self + total_other

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data):
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"{self.name}, {self.model}, {self.price} руб. Остаток: {self.quantity} шт."


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"{self.name}, {self.country}, {self.price} руб. Остаток: {self.quantity} шт."


class Category:
    name: str
    description: str
    products: list

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."

    def add_product(self, product):
        if not isinstance(product, BaseProduct):
            raise TypeError("Можно добавлять только объекты класса BaseProduct или его наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return [str(product) for product in self.__products]

    def average_price(self):
        try:
            total_price = sum(product.price for product in self.__products)
            average = total_price / len(self.__products)
            return average
        except ZeroDivisionError:
            print("В категории нет товаров, средняя цена = 0")
            return 0
