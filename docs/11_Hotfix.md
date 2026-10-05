# Hotfix: неверная сумма в `cart_total`

## Симптом
В выпущенной версии (`main`) корзина с одним мячом за 2 790 ₽ показывала итог
**2 511 ₽** — скидка 10 % применялась к любой покупке.

## Причина
Опечатка в константе: `DISCOUNT_THRESHOLD = 1000` вместо `10000`
(скидка по правилам магазина — от 10 000 ₽).

## Порядок исправления
```bash
git checkout main
git checkout -b hotfix/cart-total
# исправлена константа DISCOUNT_THRESHOLD = 10000
git commit -am "Hotfix: cart_total давал скидку от 1000 вместо 10000 руб."
git checkout main
git merge --no-ff hotfix/cart-total
git tag -a v0.1.1 -m "Hotfix: порог скидки"
git checkout develop
git merge --no-ff hotfix/cart-total
git branch -d hotfix/cart-total
```

## Проверка
| Корзина | До | После |
|---------|----|-------|
| мяч 2 790 ₽ × 1 | 2 511.00 | 2 790.00 |
| кроссовки 5 990 ₽ × 2 = 11 980 ₽ | 10 782.00 | 10 782.00 (скидка положена) |

## Почему hotfix сливается в две ветки
В `main` — чтобы исправление сразу попало пользователям; в `develop` — чтобы
следующий релиз из `develop` не вернул ошибку обратно.
