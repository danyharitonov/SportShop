"""СпортТовары — учебный магазин спортивных товаров (монолит, начало проекта).

Товар — словарь: id, name, category, brand, price, sizes {размер: остаток}.
Позиция корзины — словарь: product_id, name, size, qty, price.
"""

CATALOG = [
    {"id": 1, "name": "Кроссовки беговые Pulse", "category": "Бег", "brand": "Demix",
     "price": 5990.0, "sizes": {40: 3, 41: 4, 42: 2, 43: 1}},
    {"id": 2, "name": "Бутсы Strike FG", "category": "Футбол", "brand": "Jögel",
     "price": 4490.0, "sizes": {39: 1, 40: 1, 41: 0}},
    {"id": 3, "name": "Мяч футбольный Pro", "category": "Футбол", "brand": "Select",
     "price": 2790.0, "sizes": {5: 12}},
    {"id": 4, "name": "Рюкзак Trail 30", "category": "Туризм", "brand": "Outventure",
     "price": 3590.0, "sizes": {30: 6}},
    {"id": 5, "name": "Куртка ветрозащитная", "category": "Бег", "brand": "Demix",
     "price": 7490.0, "sizes": {46: 2, 48: 1, 50: 0}},
    {"id": 6, "name": "Коврик для йоги", "category": "Фитнес", "brand": "Torres",
     "price": 1890.0, "sizes": {183: 9}},
]

DISCOUNT_RATE = 0.10        # скидка 10 % ...
DISCOUNT_THRESHOLD = 1000   # ... на корзину от этой суммы


def find_product(products, product_id):
    return next((p for p in products if p["id"] == product_id), None)


def _position(cart, product_id, size):
    return next((it for it in cart if it["product_id"] == product_id and it["size"] == size), None)


def add_to_cart(cart, products, product_id, size, quantity):
    """Добавляет товар в корзину. Возвращает (успех, сообщение)."""
    product = find_product(products, product_id)
    if product is None:
        return False, f"Товар {product_id} не найден"
    if size not in product["sizes"]:
        return False, f"Размер {size} отсутствует у товара «{product['name']}»"
    if quantity <= 0:
        return False, "Количество должно быть положительным"
    item = _position(cart, product_id, size)
    already = item["qty"] if item else 0
    if already + quantity > product["sizes"][size]:
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
    stock = find_product(products, product_id)["sizes"][size]
    if new_qty > stock:
        return False, f"На складе только {stock} шт."
    item["qty"] = new_qty
    return True, "Количество изменено"


def cart_total(cart):
    """Сумма корзины со скидкой."""
    total = sum(it["price"] * it["qty"] for it in cart)
    if total >= DISCOUNT_THRESHOLD:
        total *= 1 - DISCOUNT_RATE
    return round(total, 2)


def show_catalog(products):
    for p in products:
        stock = sum(p["sizes"].values())
        print(f"{p['id']:>3}. {p['name']:<26} {p['category']:<8} {p['price']:>8.2f} руб.  остаток {stock}")


if __name__ == "__main__":
    show_catalog(CATALOG)
    cart = []
    print(add_to_cart(cart, CATALOG, 3, 5, 1)[1])
    print(add_to_cart(cart, CATALOG, 1, 44, 1)[1])
    print("Итого:", cart_total(cart))
