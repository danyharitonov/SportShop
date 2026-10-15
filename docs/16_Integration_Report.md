# Отчёт об интеграции (ПР №9)

## Выделенные модули

| Модуль | Ответственность | Функции |
|--------|-----------------|---------|
| `src/storage.py` | чтение/запись каталога JSON, проверка полей | `load_products`, `save_products` |
| `src/catalog.py` | поиск и сводки по каталогу | `stock_of`, `find_product`, `get_low_stock`, `highlight_low_stock`, `search_advanced`, `count_by_category`, `avg_price`, `total_sum` |
| `src/cart.py` | корзина и скидка | `add_to_cart`, `remove_from_cart`, `update_quantity`, `cart_total` |
| `src/orders.py` | заказы | `create_order`, `format_order`, `print_order`, `save_orders`, `load_orders` |
| `src/analytics.py` | статистика продаж | `total_revenue`, `average_order_total`, `best_selling_product`, `units_sold` |
| `main.py` | консольное меню | `main`, `menu_*` |
| `shop.py` | совместимость: переэкспорт функций для старых тестов | — |

## Импорты (зависимости)

```
main.py ──► storage, catalog, cart, orders, analytics
orders  ──► cart (cart_total), catalog (find_product)
cart    ──► catalog (find_product)
catalog, storage, analytics — без внутренних зависимостей
```
Циклических импортов нет; интеграция выполнялась **восходящим** способом:
`storage` и `catalog` → `cart` → `orders` → `analytics` → `main.py`.

## Интеграционные тесты (`tests/test_integration.py`, 9 шт.)

| Тест | Стык |
|------|------|
| `test_full_cycle` | загрузка → корзина → заказ → JSON → загрузка, сумма совпадает |
| `test_sizes_are_int_after_json` | storage ↔ cart |
| `test_order_text_uses_cart_fields` | cart ↔ orders |
| `test_stock_decreases_and_low_stock_reacts` | orders ↔ catalog |
| `test_analytics_over_saved_orders` | orders ↔ JSON ↔ analytics |
| `test_products_roundtrip` | storage (запись ↔ чтение) |
| `test_broken_product_file_reported` | storage: повреждённые данные |
| `test_search_then_buy_with_discount` | catalog ↔ cart (скидка) |
| `test_main_menu_smoke` | вся система через `main.py` |

## Найденные ошибки
1. Строковые размеры после JSON — исправлено в `storage.load_products`.
2. Намеренная ошибка `name` → `product` в `cart.py` — найдена тестами, исправлена
   (см. `15_Integration_Errors.md`).

## Скрипт сборки `build.py`
Пять шагов, при ошибке — выход с кодом 1:
1. `check_python_version()` — Python ≥ 3.10;
2. `check_structure()` — наличие 8 обязательных файлов;
3. `check_data()` — `data/products.json` существует и это корректный JSON;
4. `run_tests()` — `python -m unittest discover -s tests`, вывод сводки;
5. `run_app()` — проверка старта `main.py` (с ключом `--run` — интерактивный запуск).

Итог: `Сборка успешна!`, 41 тест OK.
