# Ошибки интеграции

## 1. Внесённая ошибка (намеренно)
В `src/cart.py` при добавлении позиции ключ `"name"` заменён на `"product"`:
```diff
-        cart.append({"product_id": product_id, "name": product["name"], "size": size,
+        cart.append({"product_id": product_id, "product": product["name"], "size": size,
```
Модуль `cart` сам по себе остался рабочим: `add_to_cart` и `cart_total`
не читают название, поэтому модульные тесты корзины проходят.

## 2. Как проявилась
`python -m unittest tests.test_integration`:
```
ERROR: test_analytics_over_saved_orders
  File "src/analytics.py", in best_selling_product
    sold[it["name"]] += it["qty"]
KeyError: 'name'
ERROR: test_order_text_uses_cart_fields
  File "src/orders.py", in format_order
    lines.append(f"  {it['name']:<30} ...
KeyError: 'name'
Ran 9 tests ... FAILED (errors=2)
```
Ошибка видна только на **стыке** модулей: `orders` и `analytics` ожидают
позицию корзины с полем `name`, а `cart` начал отдавать `product`.

## 3. Как исправлена
По трассировке найден модуль-источник формата (`cart.py`); формат позиции
корзины описан в его docstring (`product_id, name, size, qty, price`) —
возвращён ключ `"name"` (`git checkout src/cart.py`). Повторный прогон —
9/9 OK.

## 4. Ещё одна реальная ошибка интеграции (найдена при разделении)
После переноса каталога в `data/products.json` размеры стали строками
(`"42"`), и `add_to_cart(cart, products, 1, 42, 1)` отвечал «Размер 42
отсутствует». Исправлено в `storage.load_products`: ключи `sizes`
переводятся в `int`. Защищает тест `test_sizes_are_int_after_json`.

## Вывод
Договорённость о формате данных между модулями нужно фиксировать (docstring,
справочник API) и проверять интеграционными тестами — модульные такие
ошибки не ловят.
