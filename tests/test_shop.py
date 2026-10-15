"""Модульные тесты shop.py (ПР №8)."""
import os
import tempfile
import unittest

from shop import (add_to_cart, avg_price, cart_total, count_by_category, create_order,
                  get_low_stock, load_orders, remove_from_cart, save_orders,
                  search_advanced, total_sum, update_quantity)


def sample_products():
    """Новый список на каждый тест — тесты не влияют друг на друга."""
    return [
        {"id": 1, "name": "Кроссовки Pulse", "category": "Бег", "price": 6000.0, "sizes": {41: 2, 42: 5}},
        {"id": 2, "name": "Мяч Pro", "category": "Футбол", "price": 2500.0, "sizes": {5: 1}},
        {"id": 3, "name": "Бутсы Strike", "category": "Футбол", "price": 4500.0, "sizes": {40: 0, 41: 2}},
        {"id": 4, "name": "Рюкзак Trail", "category": "Туризм", "price": 3600.0, "sizes": {30: 10}},
    ]


class TestGetLowStock(unittest.TestCase):
    def test_empty_catalog(self):
        self.assertEqual(get_low_stock([]), [])

    def test_nothing_low(self):
        self.assertEqual(get_low_stock([{"name": "A", "sizes": {40: 10}}]), [])

    def test_sum_over_sizes_is_used(self):
        names = [p["name"] for p in get_low_stock(sample_products())]
        self.assertEqual(names, ["Мяч Pro", "Бутсы Strike"])   # 1 и 2 шт., по возрастанию

    def test_boundary_three_included(self):
        self.assertEqual(len(get_low_stock([{"name": "A", "sizes": {40: 3}}])), 1)

    def test_custom_limit(self):
        self.assertEqual(len(get_low_stock(sample_products(), limit=7)), 3)


class TestSearchAdvanced(unittest.TestCase):
    def setUp(self):
        self.products = sample_products()

    def test_by_name_case_insensitive(self):
        self.assertEqual([p["id"] for p in search_advanced(self.products, "МЯЧ")], [2])

    def test_by_category(self):
        self.assertEqual({p["id"] for p in search_advanced(self.products, category="футбол")}, {2, 3})

    def test_by_price_range_inclusive(self):
        found = search_advanced(self.products, min_price=3600, max_price=6000)
        self.assertEqual({p["id"] for p in found}, {1, 3, 4})

    def test_all_filters_together(self):
        self.assertEqual(search_advanced(self.products, "бутсы", "Футбол", 4000, 5000)[0]["id"], 3)

    def test_nothing_found(self):
        self.assertEqual(search_advanced(self.products, "лыжи"), [])


class TestTotalSum(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total_sum([]), 0)

    def test_with_quantity(self):
        self.assertEqual(total_sum([{"price": 100, "quantity": 3}, {"price": 20, "quantity": 2}]), 340)

    def test_missing_quantity_counts_as_one(self):
        self.assertEqual(total_sum([{"price": 99.5}]), 99.5)


class TestAddToCart(unittest.TestCase):
    def setUp(self):
        self.products, self.cart = sample_products(), []

    def test_invalid_size(self):
        result, message = add_to_cart(self.cart, self.products, 1, 99, 1)
        self.assertFalse(result)
        self.assertIn("размер", message.lower())

    def test_unknown_product(self):
        self.assertFalse(add_to_cart(self.cart, self.products, 42, 41, 1)[0])

    def test_success(self):
        ok, _ = add_to_cart(self.cart, self.products, 1, 42, 2)
        self.assertTrue(ok)
        self.assertEqual(self.cart[0]["qty"], 2)

    def test_repeat_increases_quantity(self):
        add_to_cart(self.cart, self.products, 1, 42, 2)
        add_to_cart(self.cart, self.products, 1, 42, 1)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]["qty"], 3)

    def test_more_than_stock(self):
        add_to_cart(self.cart, self.products, 2, 5, 1)
        ok, message = add_to_cart(self.cart, self.products, 2, 5, 1)
        self.assertFalse(ok)
        self.assertIn("только 1", message)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 1 / 0


class TestCartOperations(unittest.TestCase):
    def setUp(self):
        self.products, self.cart = sample_products(), []
        add_to_cart(self.cart, self.products, 1, 42, 1)
        add_to_cart(self.cart, self.products, 4, 30, 2)

    def test_remove(self):
        self.assertTrue(remove_from_cart(self.cart, 1, 42))
        self.assertEqual([it["product_id"] for it in self.cart], [4])
        self.assertFalse(remove_from_cart(self.cart, 1, 42))

    def test_update_quantity(self):
        ok, _ = update_quantity(self.cart, self.products, 4, 30, 5)
        self.assertTrue(ok)
        self.assertEqual(self.cart[1]["qty"], 5)

    def test_update_above_stock_rejected(self):
        self.assertFalse(update_quantity(self.cart, self.products, 1, 42, 6)[0])

    def test_update_to_zero_removes_item(self):
        update_quantity(self.cart, self.products, 1, 42, 0)
        self.assertEqual([it["product_id"] for it in self.cart], [4])

    def test_negative_quantity_rejected(self):
        ok, _ = update_quantity(self.cart, self.products, 4, 30, -2)
        self.assertFalse(ok)
        self.assertEqual(self.cart[1]["qty"], 2)

    def test_cart_total_without_discount(self):
        self.assertEqual(cart_total(self.cart), 6000 + 7200 - 1320)  # 13 200 ≥ 10 000 → −10 %

    def test_cart_total_small_no_discount(self):
        remove_from_cart(self.cart, 1, 42)
        self.assertEqual(cart_total(self.cart), 7200)

    def test_cart_total_empty(self):
        self.assertEqual(cart_total([]), 0)


class TestOrdersAndAnalytics(unittest.TestCase):
    def test_create_order_updates_stock_and_clears_cart(self):
        products, cart = sample_products(), []
        add_to_cart(cart, products, 4, 30, 3)
        order = create_order(cart, "Иванов И.", products)
        self.assertEqual(order["total"], 10800 * 0.9)
        self.assertEqual(products[3]["sizes"][30], 7)
        self.assertEqual(cart, [])

    def test_empty_cart_gives_no_order(self):
        self.assertIsNone(create_order([], "Иванов И.", sample_products()))

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "orders.json")
            save_orders([{"number": "1", "client": "Пётр", "total": 5.5}], path)
            self.assertEqual(load_orders(path)[0]["client"], "Пётр")

    def test_load_missing_file(self):
        self.assertEqual(load_orders("нет_такого_файла.json"), [])

    def test_count_and_avg(self):
        products = sample_products()
        self.assertEqual(count_by_category(products), {"Бег": 1, "Футбол": 2, "Туризм": 1})
        self.assertEqual(avg_price(products, "Футбол"), 3500)
        self.assertEqual(avg_price([]), 0)


if __name__ == "__main__":
    unittest.main()
