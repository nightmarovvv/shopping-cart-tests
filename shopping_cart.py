"""Модуль корзины покупок"""


class CartItem:
    """Позиция товара в корзине."""

    def __init__(self, name: str, price: float, quantity: int = 1) -> None:
        """Создание позиции товара.

        Args:
            name: Название товара.
            price: Цена за единицу.
            quantity: Количество единиц (по умолчанию 1).

        Raises:
            ValueError: Если название некорректно, цена отрицательная или количество <= 0.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название товара должно быть непустой строкой")
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")

        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total_price(self) -> float:
        """Возвращает стоимость позиции (price * quantity)."""
        return self.price * self.quantity


class ShoppingCart:
    """Корзина покупок.

    Поддерживает добавление товаров, удаление, применение скидок и расчет итоговой суммы.
    """

    DISCOUNT_CODES: dict[str, float] = {
        "SAVE10": 0.10,
        "SAVE50": 0.50,
    }

    def __init__(self) -> None:
        """Создать пустую корзину."""
        self._items: dict[str, CartItem] = {}
        self._discount: float = 0.0

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        """Добавить товар в корзину.

        Args:
            name: Название товара.
            price: Цена за единицу.
            quantity: Количество единиц (по умолчанию 1).

        Если товар с таким названием уже существует — увеличивает его количество.
        Цена в этом случае игнорируется (используется цена первого добавления).
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название товара должно быть непустой строкой")
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")

        if name in self._items:
            self._items[name].quantity += quantity
        else:
            self._items[name] = CartItem(name, price, quantity)

    def remove_item(self, name: str) -> None:
        """Удалить позицию из корзины.

        Raises:
            KeyError: Если товара с таким названием нет в корзине.
        """
        if name not in self._items:
            raise KeyError(f"Товар '{name}' не найден в корзине")
        del self._items[name]

    def apply_discount(self, code: str) -> bool:
        """Применить скидочный код.

        Поддерживаются только следующие коды (регистр не важен, внешние пробелы игнорируются):
        - "SAVE10" -> 10% скидка
        - "SAVE50" -> 50% скидка

        Новый валидный скидочный код полностью заменяет предыдущий.
        Невалидный скидочный код ничего не меняет и возвращает False.
        """
        normalized = code.strip().upper()
        if normalized in self.DISCOUNT_CODES:
            self._discount = self.DISCOUNT_CODES[normalized]
            return True
        return False

    def get_subtotal(self) -> float:
        """Вернуть сумму всех товаров без учета скидки."""
        return sum(item.get_total_price() for item in self._items.values())

    def get_total(self) -> float:
        """Вернуть итоговую сумму с учетом скидки, округленную до двух знаков после запятой."""
        subtotal = self.get_subtotal()
        return round(subtotal * (1 - self._discount), 2)

    def get_item_count(self) -> int:
        """Вернуть общее количество единиц товаров в корзине."""
        return sum(item.quantity for item in self._items.values())

    def clear(self) -> None:
        """Очистить корзину и сбросить примененную скидку."""
        self._items.clear()
        self._discount = 0.0

    def is_empty(self) -> bool:
        """Проверить, пуста ли корзина."""
        return len(self._items) == 0
