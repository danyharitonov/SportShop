"""Корзина покупателя.

Позиция корзины: {"product_id", "name", "size", "qty", "price"}.
"""
from src.catalog import find_product

DISCOUNT_RATE = 0.10
DISCOUNT_THRESHOLD = 10000


def _position(cart, product_id, size):
    return next((it for it in cart if it["product_id"] == product_id and it["size"] == size), None)


def add_to_cart(cart, products, product_id, size, quantity):
    """Возвращает (успех, сообщение)."""
    product = find_product(products, product_id)
    if product is None:
        return False, f"Товар {product_id} не найден"
    if size not in product["sizes"]:
        return False, f"Размер {size} отсутствует у товара «{product['name']}»"
    if quantity <= 0:
        return False, "Количество должно быть положительным"
    item = _position(cart, product_id, size)
    in_cart = item["qty"] if item else 0
    if in_cart + quantity > product["sizes"][size]:
        return False, f"На складе только {product['sizes'][size]} шт. размера {size}"
    if item:
        item["qty"] += quantity
    else:
        cart.append({"product_id": product_id, "name": product["name"], "size": size,
                     "qty": quantity, "price": product["price"]})
    return True, f"«{product['name']}» (р. {size}) × {quantity} в корзине"


def remove_from_cart(cart, product_id, size):
    item = _position(cart, product_id, size)
    if item is None:
        return False
    cart.remove(item)
    return True


def update_quantity(cart, products, product_id, size, new_qty):
    item = _position(cart, product_id, size)
    if item is None:
        return False, "Позиции нет в корзине"
    if new_qty < 0:
        return False, "Количество не может быть отрицательным"
    if new_qty == 0:
        cart.remove(item)
        return True, "Позиция удалена"
    stock = find_product(products, product_id)["sizes"][size]
    if new_qty > stock:
        return False, f"На складе только {stock} шт."
    item["qty"] = new_qty
    return True, "Количество изменено"


def cart_total(cart):
    """Сумма корзины; от DISCOUNT_THRESHOLD ₽ — скидка DISCOUNT_RATE."""
    total = sum(it["price"] * it["qty"] for it in cart)
    if total >= DISCOUNT_THRESHOLD:
        total *= 1 - DISCOUNT_RATE
    return round(total, 2)
