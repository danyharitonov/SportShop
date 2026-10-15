# Руководство разработчика

## 1. Настройка окружения
```bash
git clone [ссылка на репозиторий]
cd SportShop
python --version            # нужен 3.10+
python -m venv .venv        # необязательно: внешних зависимостей нет
.venv\Scripts\activate      # Windows   (Linux/macOS: source .venv/bin/activate)
code .                      # открыть в VS Code
```
Рекомендуемые расширения VS Code: Python, Pylance, GitLens, Markdown All in One.
Конфигурации отладки уже есть в `.vscode/launch.json`.

## 2. Запуск тестов
```bash
python -m unittest discover -s tests -v          # все 41 тест
python -m unittest tests.test_integration -v     # только интеграционные
python -m unittest tests.test_shop.TestCartOperations   # один класс
```

## 3. Как добавить новую функцию
1. Возьмите историю из `docs/03_Product_Backlog.md` (или добавьте US-N).
2. Определите модуль по ответственности: каталог → `src/catalog.py`,
   корзина → `src/cart.py`, заказы → `src/orders.py`, статистика → `src/analytics.py`.
3. Напишите функцию с docstring (назначение, параметры, результат).
4. Добавьте тест в `tests/test_shop.py` или `tests/test_integration.py`.
5. Если функция нужна пользователю — добавьте пункт в `MENU` и ветку в `main()`.
6. Опишите функцию в `docs/17_API_Reference.md`.

Правила импорта: модули `src/` импортируют друг друга только «вниз»
(`orders → cart → catalog`); `main.py` — единственный, кто вызывает `input()`/`print()` меню.

## 4. Ветки и Pull Request
```bash
git checkout develop
git pull
git checkout -b feature/<кратко-о-функции>
# ... код + тесты ...
git add .
git commit -m "US-N: что сделано"
git push -u origin feature/<...>
```
Затем создайте Pull Request `feature/<...> → develop` на GitHub (шаблон
описания — `docs/10_Pull_Request.md`). После одобрения — слияние без
fast-forward и удаление ветки. Срочные исправления — ветка `hotfix/<...>`
от `main`, слияние в `main` и `develop` (см. `docs/11_Hotfix.md`).

## 5. Сборка
```bash
python build.py
```
Шаги: версия Python → структура → данные → тесты → проверка старта `main.py`.
Код выхода 0 — «Сборка успешна!», 1 — ошибка (причина печатается).

## 6. Выпуск версии
```bash
git checkout main
git merge --no-ff develop -m "Release vX.Y"
git tag -a vX.Y -m "Релиз версии X.Y"
git push origin main --tags
```
