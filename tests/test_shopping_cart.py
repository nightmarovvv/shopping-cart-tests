"""Тесты для класса ShoppingCart."""

import pytest


class TestShoppingCartInit:

    def test_new_cart_is_empty(self, cart):
        assert cart.is_empty()
        assert cart.get_item_count() == 0
        assert cart.get_subtotal() == 0.0
        assert cart.get_total() == 0.0


class TestAddItem:
    """Добавление товаров: позитивные + негативные сценарии."""

    @pytest.mark.smoke
    def test_add_single_item(self, cart):
        cart.add_item("Яблоко", 1.50, 3)
        assert not cart.is_empty()
        assert cart.get_item_count() == 3

    def test_add_multiple_different_items(self, cart):
        cart.add_item("Яблоко", 1.50, 2)
        cart.add_item("Банан", 2.00, 3)
        assert cart.get_item_count() == 5

    def test_add_existing_item_increases_quantity(self, cart):
        cart.add_item("Яблоко", 1.50, 2)
        cart.add_item("Яблоко", 999.0, 3)  # цена должна остаться 1.50
        assert cart.get_item_count() == 5
        assert cart.get_subtotal() == 1.50 * 5

    def test_add_item_with_default_quantity(self, cart):
        cart.add_item("Яблоко", 1.50)
        assert cart.get_item_count() == 1

    @pytest.mark.parametrize(
        ("name", "price", "quantity", "expected_error"),
        [
            ("", 1.0, 1, "Название товара должно быть непустой строкой"),
            ("   ", 1.0, 1, "Название товара должно быть непустой строкой"),
            (None, 1.0, 1, "Название товара должно быть непустой строкой"),
            ("Яблоко", -1.0, 1, "Цена не может быть отрицательной"),
            ("Яблоко", 1.0, 0, "Количество должно быть положительным"),
            ("Яблоко", 1.0, -5, "Количество должно быть положительным"),
        ],
        ids=[
            "empty_name",
            "whitespace_name",
            "none_name",
            "negative_price",
            "zero_quantity",
            "negative_quantity",
        ],
    )
    def test_add_item_with_invalid_params_raises_value_error(
        self, cart, name, price, quantity, expected_error
    ):
        with pytest.raises(ValueError, match=expected_error):
            cart.add_item(name, price, quantity)

    def test_add_invalid_item_does_not_modify_cart(self, cart):
        """Проверяем, что при ошибке валидации корзина не меняется."""
        cart.add_item("Яблоко", 1.50, 2)
        with pytest.raises(ValueError):
            cart.add_item("", 1.0, 1)
        assert cart.get_item_count() == 2


class TestRemoveItem:

    def test_remove_existing_item(self, cart):
        cart.add_item("Яблоко", 1.50)
        cart.remove_item("Яблоко")
        assert cart.is_empty()

    def test_remove_one_of_many_items(self, cart_with_items):
        initial_count = cart_with_items.get_item_count()
        cart_with_items.remove_item("Яблоко")  # убираем 3 шт.
        assert cart_with_items.get_item_count() == initial_count - 3

    def test_remove_nonexistent_item_raises_key_error(self, cart):
        with pytest.raises(KeyError) as exc_info:
            cart.remove_item("Несуществующий")
        assert "Несуществующий" in exc_info.value.args[0]

    def test_remove_from_empty_cart_raises_key_error(self, cart):
        with pytest.raises(KeyError):
            cart.remove_item("Яблоко")


class TestApplyDiscount:

    @pytest.mark.parametrize(
        ("code", "expected_total_ratio"),
        [
            ("SAVE10", 0.90),
            ("SAVE50", 0.50),
        ],
        ids=["save10_10_percent", "save50_50_percent"],
    )
    def test_valid_discount_code(self, cart, code, expected_total_ratio):
        cart.add_item("Товар", 100.0)
        assert cart.apply_discount(code) is True
        assert cart.get_total() == 100.0 * expected_total_ratio

    def test_invalid_discount_code_returns_false(self, cart):
        assert cart.apply_discount("INVALID") is False

    def test_discount_code_case_insensitive(self, cart):
        cart.add_item("Товар", 100.0)
        assert cart.apply_discount("save10") is True
        assert cart.get_total() == 90.0

    def test_discount_code_strips_whitespace(self, cart):
        cart.add_item("Товар", 100.0)
        assert cart.apply_discount("  SAVE10  ") is True
        assert cart.get_total() == 90.0

    def test_new_valid_discount_replaces_previous(self, cart):
        cart.add_item("Товар", 100.0)
        cart.apply_discount("SAVE10")
        cart.apply_discount("SAVE50")
        assert cart.get_total() == 50.0

    def test_invalid_code_does_not_replace_existing_discount(self, cart):
        cart.add_item("Товар", 100.0)
        cart.apply_discount("SAVE10")
        cart.apply_discount("INVALID")
        assert cart.get_total() == 90.0


class TestGetSubtotal:

    def test_empty_cart_subtotal_is_zero(self, cart):
        assert cart.get_subtotal() == 0.0

    def test_subtotal_sums_all_items(self, cart_with_items):
        # 1.50*3 + 2.00*2 + 3.50*1 = 12.0
        assert cart_with_items.get_subtotal() == 12.0

    def test_subtotal_ignores_discount(self, cart_with_items):
        cart_with_items.apply_discount("SAVE50")
        assert cart_with_items.get_subtotal() == 12.0


class TestGetTotal:

    @pytest.mark.smoke
    def test_total_without_discount_equals_subtotal(self, cart_with_items):
        assert cart_with_items.get_total() == cart_with_items.get_subtotal()

    @pytest.mark.smoke
    def test_total_with_discount(self, cart_with_items):
        cart_with_items.apply_discount("SAVE10")
        assert cart_with_items.get_total() == round(12.0 * 0.9, 2)

    def test_total_with_50_percent_discount(self, cart_with_items):
        cart_with_items.apply_discount("SAVE50")
        assert cart_with_items.get_total() == 6.0

    def test_total_rounds_to_two_decimal_places(self, cart):
        cart.add_item("Товар", 10.33, 3)  # subtotal = 30.99
        cart.apply_discount("SAVE10")      # 30.99 * 0.9 = 27.891
        assert cart.get_total() == 27.89

    def test_total_empty_cart_with_discount_is_zero(self, cart):
        cart.apply_discount("SAVE50")
        assert cart.get_total() == 0.0


class TestGetItemCount:

    def test_empty_cart_count_is_zero(self, cart):
        assert cart.get_item_count() == 0

    def test_count_sums_all_quantities(self, cart_with_items):
        # 3 + 2 + 1 = 6
        assert cart_with_items.get_item_count() == 6

    def test_count_after_adding_items(self, cart):
        cart.add_item("Яблоко", 1.0, 5)
        cart.add_item("Банан", 2.0, 3)
        assert cart.get_item_count() == 8


class TestClear:

    def test_clear_removes_all_items(self, cart_with_items):
        cart_with_items.clear()
        assert cart_with_items.is_empty()
        assert cart_with_items.get_item_count() == 0
        assert cart_with_items.get_subtotal() == 0.0

    def test_clear_resets_discount(self, cart_with_items):
        cart_with_items.apply_discount("SAVE50")
        cart_with_items.clear()
        cart_with_items.add_item("Товар", 100.0)
        assert cart_with_items.get_total() == 100.0

    def test_clear_empty_cart_no_error(self, cart):
        cart.clear()
        assert cart.is_empty()


class TestIsEmpty:

    def test_new_cart_is_empty(self, cart):
        assert cart.is_empty() is True

    def test_cart_with_items_is_not_empty(self, cart_with_items):
        assert cart_with_items.is_empty() is False

    def test_cart_empty_after_removing_last_item(self, cart):
        cart.add_item("Яблоко", 1.0)
        cart.remove_item("Яблоко")
        assert cart.is_empty() is True

    def test_cart_empty_after_clear(self, cart_with_items):
        cart_with_items.clear()
        assert cart_with_items.is_empty() is True


class TestEndToEnd:
    """E2E-сценарии через фабрику фикстур — полный флоу корзины."""

    def test_full_purchase_flow(self, make_cart):
        """Полный сценарий: добавление -> скидка -> проверка итога -> очистка."""
        cart = make_cart(
            items=[("Ноутбук", 50000.0, 1), ("Мышь", 1500.0, 2), ("Кабель", 300.0, 3)],
            discount_code="SAVE10",
        )
        expected_subtotal = 50000.0 + 1500.0 * 2 + 300.0 * 3
        assert cart.get_subtotal() == expected_subtotal
        assert cart.get_total() == round(expected_subtotal * 0.9, 2)
        assert cart.get_item_count() == 6

        cart.remove_item("Кабель")
        assert cart.get_item_count() == 3

        cart.clear()
        assert cart.is_empty()
        assert cart.get_total() == 0.0

    def test_discount_switch_during_shopping(self, make_cart):
        cart = make_cart(items=[("Товар А", 200.0, 1), ("Товар Б", 300.0, 1)])
        assert cart.get_total() == 500.0

        cart.apply_discount("SAVE10")
        assert cart.get_total() == 450.0

        # покупатель нашёл код получше
        cart.apply_discount("SAVE50")
        assert cart.get_total() == 250.0

        # пробует невалидный — скидка не слетает
        cart.apply_discount("FREEBIE")
        assert cart.get_total() == 250.0
