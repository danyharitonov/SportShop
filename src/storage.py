"""Хранилище: чтение и запись каталога в JSON.

В JSON ключи словаря всегда строки, поэтому размеры ("42") при загрузке
переводятся обратно в int — иначе add_to_cart(…, size=42) их не найдёт.
"""
import json

REQUIRED = ("id", "name", "category", "price", "sizes")


def load_products(filename="data/products.json"):
    with open(filename, encoding="utf-8") as fh:
        raw = json.load(fh)
    products = []
    for item in raw:
        missing = [key for key in REQUIRED if key not in item]
        if missing:
            raise ValueError(f"товар {item.get('id', '?')}: нет полей {missing}")
        item["sizes"] = {int(size): int(qty) for size, qty in item["sizes"].items()}
        products.append(item)
    return products


def save_products(products, filename="data/products.json"):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(products, fh, ensure_ascii=False, indent=2)
    return len(products)
