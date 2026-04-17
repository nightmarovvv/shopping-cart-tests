import pytest

from shopping_cart import CartItem, ShoppingCart


@pytest.fixture()
def cart() -> ShoppingCart:
    return ShoppingCart()


@pytest.fixture()
def sample_cart_item() -> CartItem:
    return CartItem("Яблоко", 1.50, 3)


@pytest.fixture()
def cart_with_items() -> ShoppingCart:
    """Корзина: Яблоко 1.50*3 + Банан 2.00*2 + Молоко 3.50*1 = 12.00."""
    cart = ShoppingCart()
    cart.add_item("Яблоко", 1.50, 3)
    cart.add_item("Банан", 2.00, 2)
    cart.add_item("Молоко", 3.50, 1)
    return cart


@pytest.fixture()
def make_cart():
    """Фабрика корзин — позволяет собрать корзину с произвольным набором товаров и скидкой."""

    def _make_cart(items=None, discount_code=None):
        cart = ShoppingCart()
        for name, price, qty in (items or []):
            cart.add_item(name, price, qty)
        if discount_code:
            cart.apply_discount(discount_code)
        return cart

    return _make_cart
