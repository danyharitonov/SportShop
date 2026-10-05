# Разрешение конфликта слияния в `total_sum`

## Как возник конфликт
1. От `develop` созданы две ветки: `feature/total-v1` и `feature/total-v2`.
2. В обеих ветках в одно и то же место `shop.py` добавлена функция `total_sum`:
   - v1 — `sum(p["price"] for p in products)` (без количества);
   - v2 — `sum(p["price"] * p["quantity"] for p in products)`.
3. `git merge feature/total-v1` прошёл как fast-forward.
4. `git merge feature/total-v2` остановился: `CONFLICT (content): Merge conflict in shop.py`.

## Маркеры в файле
```
<<<<<<< HEAD
    """US-7: сумма цен позиций."""
    return sum(p["price"] for p in products)
=======
    """US-7: сумма позиций с учётом количества."""
    return sum(p["price"] * p["quantity"] for p in products)
>>>>>>> feature/total-v2
```
Между `<<<<<<<` и `=======` — версия текущей ветки (`develop`, уже содержащей v1),
между `=======` и `>>>>>>>` — входящая версия из `feature/total-v2`.

## Решение
По критерию приёмки US-7 сумма должна учитывать количество, поэтому оставлена
логика v2. Дополнительно `p.get("quantity", 1)` — позиция без поля количества
считается за 1 шт. (так `total_sum` не падает с `KeyError` на списке товаров).

```python
def total_sum(products):
    """US-7: сумма позиций с учётом количества (если quantity нет — 1 шт.)."""
    return sum(p["price"] * p.get("quantity", 1) for p in products)
```

Проверка: `total_sum([{"price": 100, "quantity": 3}, {"price": 50}])` → `350`.

## Завершение
```
git add shop.py
git commit -m "Разрешён конфликт в total_sum"
git branch -d feature/total-v1 feature/total-v2
```

## Вывод
Конфликт возникает, когда две ветки меняют одни и те же строки. Git не выбирает
версию сам — решение принимает разработчик по требованиям задачи.
