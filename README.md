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

## Установка

```bash
pip install pytest pytest-cov ruff
```

## Запуск

```bash
# тесты
pytest

# тесты + покрытие
pytest --cov=shopping_cart --cov-report=term-missing

# линтер
ruff check .
```
