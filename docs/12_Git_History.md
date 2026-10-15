# История коммитов (git log --oneline --graph --all)

```
* 91b0e65 Day 7: описание hotfix
*   c3de7ee Merge hotfix/cart-total в develop
|\  
* \   aa05070 Merge PR: feature/search-advanced → develop (US-2)
|\ \  
| * | 85af293 Day 7: описание Pull Request feature/search-advanced
| * | cad7fe5 US-2: добавлена функция search_advanced
|/ /  
* | cef1638 Day 7: описание разрешения конфликта
* |   47e4db0 Разрешён конфликт в total_sum
|\ \  
| * | cb0aeaa US-7: total_sum — цена × количество (v2)
* | | d0ad7a5 US-7: total_sum — сумма цен (v1)
|/ /  
* | 17373b5 US-1: добавлена функция get_low_stock
* | 55074bc Day 7: схема Git Flow
| | * f82a358 Merge hotfix/cart-total в main
| |/| 
|/|/  
| * bd43e21 Hotfix: cart_total давал скидку от 1000 вместо 10000 руб.
|/  
* d104cfd Day 6: kanban-доска, стендап и ретроспектива
* 3467872 US-4: оформление заказа, save_orders и load_orders
* a95965c US-5, US-6: добавлены функции count_by_category и avg_price
* 1de40bf Day 6: product backlog и sprint backlog
* 87e4266 ПР5: каркас магазина СпортТовары — каталог и корзина
* a5a261e ПР5: основы Python, задания 1-8 и дополнительное (Чудо Обувь)
* 8e3c7b4 ПР4: объектная модель туроператора и тесты
* c2ae568 ПР3: эскизный и технический проект, диаграммы
* 40f7581 ПР2: техническое задание ИС ТурОфис
* 40ae379 ПР1: анализ предметной области (туроператор)
```

## Анализ графа

**Сколько веток было создано?** Шесть, кроме `main`: `develop`,
`feature/low-stock`, `feature/total-v1`, `feature/total-v2`,
`feature/search-advanced`, `hotfix/cart-total`. После слияния все временные
ветки удалены, остались `main` и `develop`.

**Какие слияния произошли?**
1. `feature/low-stock` → `develop` — fast-forward (в графе это прямая линия).
2. `feature/total-v1` → `develop` — fast-forward.
3. `feature/total-v2` → `develop` — слияние с конфликтом, коммит «Разрешён конфликт в total_sum».
4. `feature/search-advanced` → `develop` — `--no-ff`, коммит «Merge PR …» (имитация Pull Request).
5. `hotfix/cart-total` → `main` (с тегом `v0.1.1`) и → `develop`.

**Был ли конфликт и как он разрешён?** Да — в функции `total_sum`: обе ветки
total добавили разные реализации в одно место `shop.py`. Оставлена версия с
учётом количества (подробно — `docs/09_Conflict_Resolution.md`).
