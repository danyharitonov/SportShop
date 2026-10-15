# Pull Request

## PR: feature/search-advanced → develop

**Что сделано:** добавлена функция `search_advanced(products, query="", category=None,
min_price=None, max_price=None)` — поиск по части названия (без учёта регистра),
категории и диапазону цены; любой фильтр можно опустить.

**Как проверить:**
```bash
git checkout feature/search-advanced
python -c "import shop; print([p['name'] for p in shop.search_advanced(shop.CATALOG, '', 'футбол', max_price=4000)])"
# ожидается: ['Мяч футбольный Pro']
```

**Связанные задачи:** US-2

**Ревьюер:** [ФИО руководителя]

**Чек-лист ревью:**
- [x] имя и параметры совпадают с backlog;
- [x] границы цены включаются (`min_price <= price <= max_price`);
- [x] нет изменений вне `shop.py`;
- [x] слияние без конфликтов.

**Результат ревью:** одобрено, слияние с `--no-ff`.
