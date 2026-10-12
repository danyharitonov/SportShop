"""Интеграционные тесты: модули src/ работают вместе (ПР №9)."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from src.analytics import best_selling_product, total_revenue
from src.cart import add_to_cart, cart_total
from src.catalog import get_low_stock, search_advanced
from src.orders import create_order, format_order, load_orders, save_orders
from src.storage import load_products, save_products

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS = os.path.join(ROOT, "data", "products.json")


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.products = load_products(PRODUCTS)
        self.cart = []
        self.tmp = tempfile.mkdtemp()
        self.orders_file = os.path.join(self.tmp, "test_orders.json")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_full_cycle(self):
        ok, _ = add_to_cart(self.cart, self.products, 1, 40, 2)
        self.assertTrue(ok)
        order = create_order(self.cart, "Тестовый клиент", self.products)
        self.assertIsNotNone(order)
        self.assertGreater(order["total"], 0)
        save_orders([order], self.orders_file)
        loaded = load_orders(self.orders_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["total"], order["total"])

    def test_sizes_are_int_after_json(self):
        """Стык storage ↔ cart: размер 42 из JSON должен находиться как int."""
        self.assertIn(42, self.products[0]["sizes"])
        self.assertTrue(add_to_cart(self.cart, self.products, 1, 42, 1)[0])

    def test_order_text_uses_cart_fields(self):
        """Стык cart ↔ orders: format_order читает поля позиции корзины."""
        add_to_cart(self.cart, self.products, 3, 5, 2)
        text = format_order(create_order(self.cart, "Анна", self.products))
        self.assertIn("Мяч футбольный Pro", text)
        self.assertIn("5580.00", text)

    def test_stock_decreases_and_low_stock_reacts(self):
        before = {p["id"] for p in get_low_stock(self.products)}
        add_to_cart(self.cart, self.products, 4, 30, 4)          # рюкзаков 6 → 2
        create_order(self.cart, "Олег", self.products)
        after = {p["id"] for p in get_low_stock(self.products)}
        self.assertEqual(after - before, {4})

    def test_analytics_over_saved_orders(self):
        orders = []
        for client, (pid, size, qty) in {"А": (3, 5, 3), "Б": (6, 183, 1), "В": (3, 5, 1)}.items():
            add_to_cart(self.cart, self.products, pid, size, qty)
            orders.append(create_order(self.cart, client, self.products))
        save_orders(orders, self.orders_file)
        loaded = load_orders(self.orders_file)
        self.assertEqual(best_selling_product(loaded), ("Мяч футбольный Pro", 4))
        self.assertEqual(total_revenue(loaded), round(2790 * 3 + 1890 + 2790, 2))

    def test_products_roundtrip(self):
        path = os.path.join(self.tmp, "p.json")
        save_products(self.products, path)
        self.assertEqual(load_products(path), self.products)

    def test_broken_product_file_reported(self):
        path = os.path.join(self.tmp, "bad.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump([{"id": 1, "name": "без цены"}], fh)
        with self.assertRaises(ValueError):
            load_products(path)

    def test_search_then_buy_with_discount(self):
        tent = search_advanced(self.products, "палатка")[0]
        add_to_cart(self.cart, self.products, tent["id"], 2, 2)   # 17 980 ₽ → −10 %
        self.assertEqual(cart_total(self.cart), 16182.0)

    def test_main_menu_smoke(self):
        """Система целиком: main.py запускается и выходит по пункту 0."""
        work = os.path.join(self.tmp, "app")
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        res = subprocess.run([sys.executable, "main.py"], cwd=work, input="1\n3\n0\n",
                             capture_output=True, text=True, timeout=20)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Палатка Dome 2", res.stdout)
        self.assertIn("До свидания!", res.stdout)


if __name__ == "__main__":
    unittest.main()
