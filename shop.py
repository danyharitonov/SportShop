"""Совместимость со старым монолитом (ПР №5–8).

После ПР №9 весь код живёт в пакете src/. Этот модуль только
переэкспортирует функции, чтобы старые тесты и сценарии работали без правок.
"""
import os

from src.analytics import average_order_total, best_selling_product, total_revenue  # noqa: F401
from src.cart import (DISCOUNT_RATE, DISCOUNT_THRESHOLD, add_to_cart, cart_total,  # noqa: F401
                      remove_from_cart, update_quantity)
from src.catalog import (avg_price, count_by_category, find_product, get_low_stock,  # noqa: F401
                         highlight_low_stock, search_advanced, total_sum)
from src.orders import create_order, load_orders, save_orders  # noqa: F401
from src.storage import load_products

CATALOG = load_products(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "products.json"))
