"""Заказы: оформление, печать, сохранение в JSON."""
import json
from datetime import datetime

from src.cart import cart_total
from src.catalog import find_product


def create_order(cart, client_name, products):
    """Создаёт заказ, списывает остатки и очищает корзину. Пустая корзина → None."""
    if not cart or not client_name.strip():
        return None
    for it in cart:
        find_product(products, it["product_id"])["sizes"][it["size"]] -= it["qty"]
    now = datetime.now()
    order = {
        "number": now.strftime("SP-%Y%m%d-%H%M%S%f")[:-3],
        "date": now.strftime("%Y-%m-%d %H:%M"),
        "client": client_name.strip(),
        "items": [dict(it) for it in cart],
        "total": cart_total(cart),
    }
    cart.clear()
    return order


def format_order(order):
    lines = [f"Заказ {order['number']} от {order['date']}, клиент: {order['client']}"]
    for it in order["items"]:
        lines.append(f"  {it['name']:<30} р.{it['size']:<4} {it['qty']} × {it['price']:.2f}")
    lines.append(f"  ИТОГО: {order['total']:.2f} руб.")
    return "\n".join(lines)


def print_order(order):
    print(format_order(order))


def save_orders(orders, filename="data/orders.json"):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(orders, fh, ensure_ascii=False, indent=2)
    return len(orders)


def load_orders(filename="data/orders.json"):
    try:
        with open(filename, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return []
