# Справочник API

Все функции работают со структурами:
- **товар** — `{"id": int, "name": str, "category": str, "brand": str, "price": float, "sizes": {int: int}}`;
- **позиция корзины** — `{"product_id": int, "name": str, "size": int, "qty": int, "price": float}`;
- **заказ** — `{"number": str, "date": str, "client": str, "items": [позиции], "total": float}`.

---

## Модуль `src/storage.py`

### `load_products(filename="data/products.json")`
Загружает каталог из JSON и приводит ключи `sizes` к `int`.

**Параметры:** `filename` (str) — путь к файлу.
**Возвращает:** `list[dict]` — список товаров.
**Пример:**
```python
products = load_products("data/products.json")
print(len(products))          # 10
```
**Исключения:** `FileNotFoundError` — нет файла; `json.JSONDecodeError` — повреждён JSON;
`ValueError` — у товара нет обязательного поля (`id, name, category, price, sizes`).

### `save_products(products, filename="data/products.json")`
Записывает каталог в JSON (UTF-8, отступ 2).
**Параметры:** `products` (list[dict]), `filename` (str).
**Возвращает:** `int` — число записанных товаров.
**Пример:** `save_products(products)`
**Исключения:** `OSError` — нет прав на запись.

---

## Модуль `src/catalog.py`

### `get_low_stock(products, limit=3)`
Возвращает товары с суммарным остатком ≤ `limit`, отсортированные по остатку.
**Параметры:** `products` (list[dict]) — список товаров; `limit` (int) — порог.
**Возвращает:** `list[dict]`.
**Пример:**
```python
low = get_low_stock(products)
for p in low:
    print(p["name"])
```
**Исключения:** `KeyError` — у товара нет `sizes`.

### `search_advanced(products, query="", category=None, min_price=None, max_price=None)`
Комбинированный поиск; `None`/пустая строка — фильтр не применяется. Название и
категория сравниваются без учёта регистра, границы цены включаются.
**Возвращает:** `list[dict]`.
**Пример:** `search_advanced(products, "мяч", max_price=3000)` → `[Мяч футбольный Pro]`
**Исключения:** нет.

### `count_by_category(products)`
**Возвращает:** `dict[str, int]` — количество наименований в каждой категории.
**Пример:** `{'Бег': 2, 'Футбол': 2, 'Туризм': 2, 'Фитнес': 2, 'Баскетбол': 2}`
**Исключения:** `KeyError` — нет поля `category`.

### `avg_price(products, category=None)`
Средняя цена каталога или категории, округлённая до копеек; пустой набор — `0`.
**Пример:** `avg_price(products, "Бег")` → `6740.0`
**Исключения:** нет.

### `total_sum(products)`
Сумма `price × quantity`; позиция без `quantity` считается за 1 шт.
**Пример:** `total_sum([{"price": 100, "quantity": 3}, {"price": 50}])` → `350`
**Исключения:** `KeyError` — нет `price`.

### `find_product(products, product_id)`
**Возвращает:** товар с данным `id` или `None`.
**Пример:** `find_product(products, 3)["name"]` → `'Мяч футбольный Pro'`

---

## Модуль `src/cart.py`

### `add_to_cart(cart, products, product_id, size, quantity)`
Добавляет товар; при повторном добавлении увеличивает количество.
**Возвращает:** `tuple[bool, str]` — успех и сообщение для пользователя.
**Пример:**
```python
ok, msg = add_to_cart(cart, products, 1, 42, 2)
print(msg)   # «Кроссовки беговые Pulse» (р. 42) × 2 в корзине
```
**Ошибки (возвращается False):** нет товара; нет размера; количество ≤ 0; больше остатка.

### `remove_from_cart(cart, product_id, size)`
**Возвращает:** `True`, если позиция удалена, иначе `False`.

### `update_quantity(cart, products, product_id, size, new_qty)`
Меняет количество; `0` — удаляет позицию; отрицательное и больше остатка — отказ.
**Возвращает:** `tuple[bool, str]`.
**Пример:** `update_quantity(cart, products, 3, 5, 1)` → `(True, 'Количество изменено')`

### `cart_total(cart)`
Сумма корзины; при сумме ≥ 10 000 ₽ — скидка 10 %.
**Пример:** 2 × 5 990 + 1 × 2 790 = 14 770 → `13293.0`
**Исключения:** нет (пустая корзина — `0`).

---

## Модуль `src/orders.py`

### `create_order(cart, client_name, products)`
Создаёт заказ, списывает остатки, очищает корзину.
**Возвращает:** `dict` заказа или `None` (пустая корзина / пустое имя).
**Пример:** `order = create_order(cart, "Смирнова Ольга", products); order["total"]`

### `format_order(order)` / `print_order(order)`
Текстовый чек заказа (строка) / вывод его на экран.

### `save_orders(orders, filename="data/orders.json")`
**Возвращает:** `int` — число заказов. **Исключения:** `OSError`.

### `load_orders(filename="data/orders.json")`
**Возвращает:** `list[dict]`; нет файла — `[]`. **Исключения:** `json.JSONDecodeError`.

---

## Модуль `src/analytics.py`

### `total_revenue(orders)`
**Возвращает:** `float` — сумма `total` всех заказов.

### `average_order_total(orders)`
**Возвращает:** средний чек; нет заказов — `0`.

### `best_selling_product(orders)`
**Возвращает:** `(название, штук)` самого продаваемого товара или `None`.
**Пример:** `('Мяч футбольный Pro', 4)`

### `units_sold(orders)`
**Возвращает:** общее число проданных единиц.
