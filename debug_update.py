"""Воспроизведение ошибки update_quantity(…, 0) для отладчика (ПР №8)."""
from shop import CATALOG, add_to_cart, update_quantity

cart = []
add_to_cart(cart, CATALOG, 1, 42, 1)
print(update_quantity(cart, CATALOG, 1, 42, 0))
print("Корзина после обнуления:", cart)
