"""Каталог: поиск, остатки, сводки по товарам."""


def stock_of(product):
    """Суммарный остаток товара по всем размерам."""
    return sum(product["sizes"].values())


def find_product(products, product_id):
    return next((p for p in products if p["id"] == product_id), None)


def get_low_stock(products, limit=3):
    """US-1: товары с остатком <= limit, по возрастанию остатка."""
    return sorted((p for p in products if stock_of(p) <= limit), key=stock_of)


def highlight_low_stock(products, limit=3):
    return [f"⚠ {p['name']} — осталось {stock_of(p)}" for p in get_low_stock(products, limit)]


def search_advanced(products, query="", category=None, min_price=None, max_price=None):
    """US-2: комбинированный поиск; None означает «фильтр не задан»."""
    query = query.strip().lower()

    def fits(p):
        return ((not query or query in p["name"].lower())
                and (category is None or p["category"].lower() == category.lower())
                and (min_price is None or p["price"] >= min_price)
                and (max_price is None or p["price"] <= max_price))

    return [p for p in products if fits(p)]


def count_by_category(products):
    """US-5: {категория: количество наименований}."""
    counts = {}
    for p in products:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    return counts


def avg_price(products, category=None):
    """US-6: средняя цена (всего каталога или категории)."""
    prices = [p["price"] for p in products if category in (None, p["category"])]
    return round(sum(prices) / len(prices), 2) if prices else 0


def total_sum(products):
    """US-7: сумма price × quantity (нет quantity — 1 шт.)."""
    return sum(p["price"] * p.get("quantity", 1) for p in products)
