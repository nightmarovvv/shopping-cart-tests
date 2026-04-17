"""Тесты для класса CartItem."""

import pytest

from shopping_cart import CartItem


class TestCartItemCreation:
    """Позитивные и негативные сценарии создания CartItem."""

    def test_create_with_default_quantity(self):
        item = CartItem("Яблоко", 1.50)
        assert item.name == "Яблоко"
        assert item.price == 1.50
        assert item.quantity == 1

    def test_create_with_custom_quantity(self):
        item = CartItem("Яблоко", 1.50, 5)
        assert item.name == "Яблоко"
        assert item.price == 1.50
        assert item.quantity == 5

    def test_create_with_zero_price(self):
        item = CartItem("Подарок", 0)
        assert item.price == 0

    @pytest.mark.parametrize(
        ("name", "price", "quantity", "expected_error"),
        [
            ("", 1.0, 1, "Название товара должно быть непустой строкой"),
            ("   ", 1.0, 1, "Название товара должно быть непустой строкой"),
            (None, 1.0, 1, "Название товара должно быть непустой строкой"),
            (123, 1.0, 1, "Название товара должно быть непустой строкой"),
            ("Яблоко", -1.0, 1, "Цена не может быть отрицательной"),
            ("Яблоко", 1.0, 0, "Количество должно быть положительным"),
            ("Яблоко", 1.0, -5, "Количество должно быть положительным"),
        ],
        ids=[
            "empty_name",
            "whitespace_name",
            "none_name",
            "int_name",
            "negative_price",
            "zero_quantity",
            "negative_quantity",
        ],
    )
    def test_create_with_invalid_params_raises_value_error(
        self, name, price, quantity, expected_error
    ):
        with pytest.raises(ValueError, match=expected_error):
            CartItem(name, price, quantity)


class TestCartItemTotalPrice:

    @pytest.mark.parametrize(
        ("price", "quantity", "expected"),
        [
            (10.0, 1, 10.0),
            (2.50, 4, 10.0),
            (0, 5, 0),
            (99.99, 3, pytest.approx(299.97)),
        ],
        ids=["single_item", "multiple_items", "zero_price", "float_precision"],
    )
    def test_total_price_calculation(self, price, quantity, expected):
        item = CartItem("Товар", price, quantity)
        assert item.get_total_price() == expected

    def test_total_price_with_fixture(self, sample_cart_item):
        # 1.50 * 3 = 4.50
        assert sample_cart_item.get_total_price() == 4.50
