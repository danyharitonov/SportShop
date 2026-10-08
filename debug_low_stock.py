"""Сценарий для отладки get_low_stock (ПР №8): python -m pdb debug_low_stock.py"""
from shop import CATALOG, get_low_stock

print([p["name"] for p in get_low_stock(CATALOG)])
