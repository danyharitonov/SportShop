import unittest
from datetime import date

from turofis.models import Client, Manager, Tour, TourKind, TourStatus, Voucher
from turofis.operator import TourOperator


def make_operator():
    op = TourOperator("Горизонт")
    m = Manager(1, "Иванова А.С.", "1")
    op.add_tour(Tour("T-1", "Кольцо", "Ярославль", TourKind.EXCURSION,
                     date(2026, 5, 1), date(2026, 5, 5), 10000, m))
    op.add_quota("T-1", "Отель", 5)
    op.publish("T-1")
    return op


class TestModels(unittest.TestCase):
    def test_bad_passport(self):
        with self.assertRaises(ValueError):
            Client(1, "Петров Пётр", "12345")

    def test_dates_order(self):
        with self.assertRaises(ValueError):
            Tour("T", "x", "y", TourKind.BEACH, date(2026, 5, 5), date(2026, 5, 1), 1, None)

    def test_bulk_discount(self):
        self.assertEqual(Voucher.calc_amount(1000, 3), 3000)
        self.assertEqual(Voucher.calc_amount(1000, 4), 3800)

    def test_partial_payment(self):
        op = make_operator()
        v = op.sell("T-1", "Петров Пётр", "4510 123456", 1)
        self.assertEqual(v.pay(4000), "частично оплачена")
        self.assertEqual(v.pay(6000), "оплачена")
        with self.assertRaises(ValueError):
            v.pay(1)


class TestOperator(unittest.TestCase):
    def test_no_overselling(self):
        op = make_operator()
        op.sell("T-1", "Петров Пётр", "4510 123456", 5)
        self.assertIs(op.tours["T-1"].status, TourStatus.SOLD_OUT)
        with self.assertRaises(ValueError):
            op.sell("T-1", "Иванов Иван", "4510 000001", 1)

    def test_refund_returns_seats(self):
        op = make_operator()
        v = op.sell("T-1", "Петров Пётр", "4510 123456", 5)
        op.refund(v.number)
        self.assertEqual(op.tours["T-1"].seats_left, 5)
        self.assertIs(op.tours["T-1"].status, TourStatus.ON_SALE)

    def test_same_client_reused(self):
        op = make_operator()
        op.sell("T-1", "Петров Пётр", "4510 123456", 1)
        op.sell("T-1", "Петров Пётр", "4510 123456", 1)
        self.assertEqual(len(op.clients), 1)

    def test_review_only_after_finish(self):
        op = make_operator()
        v = op.sell("T-1", "Петров Пётр", "4510 123456", 1)
        with self.assertRaises(ValueError):
            op.leave_review(v.number, 5)
        op.tours["T-1"].status = TourStatus.FINISHED
        op.leave_review(v.number, 5)
        self.assertEqual(op.avg_rating("T-1"), 5)


if __name__ == "__main__":
    unittest.main()
