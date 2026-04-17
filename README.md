# Shopping Cart Tests

Тесты для модуля `shopping_cart.py` (классы `CartItem` и `ShoppingCart`).

## Структура

```
├── shopping_cart.py
├── tests/
│   ├── conftest.py
│   ├── test_cart_item.py
│   └── test_shopping_cart.py
├── pyproject.toml
└── README.md
```

## Установка и запуск

```bash
git clone https://github.com/nightmarovvv/shopping-cart-tests.git
cd shopping-cart-tests
python3 -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov ruff
```

```bash
# тесты
pytest

# тесты + покрытие
pytest --cov=shopping_cart --cov-report=term-missing

# только smoke
pytest -m smoke

# линтер
ruff check .
```
