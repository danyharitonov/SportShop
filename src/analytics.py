"""Аналитика продаж по списку заказов."""
from collections import Counter


def total_revenue(orders):
    """US-8: выручка — сумма total всех заказов."""
    return round(sum(o["total"] for o in orders), 2)


def average_order_total(orders):
    """US-8: средний чек."""
    return round(total_revenue(orders) / len(orders), 2) if orders else 0


def best_selling_product(orders):
    """US-9: (название, штук) самого продаваемого товара или None."""
    sold = Counter()
    for order in orders:
        for it in order["items"]:
            sold[it["name"]] += it["qty"]
    return sold.most_common(1)[0] if sold else None


def units_sold(orders):
    return sum(it["qty"] for o in orders for it in o["items"])
