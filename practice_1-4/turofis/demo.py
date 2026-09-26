"""Демонстрация объектной модели: python -m turofis.demo (из папки practice_1-4)."""
from datetime import date

from .models import Manager, Tour, TourKind, TourStatus
from .operator import TourOperator


def main():
    op = TourOperator("Горизонт")
    ivanova = Manager(1, "Иванова А.С.", "+7 900 111-22-33")
    ring = op.add_tour(Tour("T-001", "Золотое кольцо", "Ярославль", TourKind.EXCURSION,
                            date(2026, 5, 10), date(2026, 5, 15), 32000, ivanova))
    op.add_tour(Tour("T-002", "Байкал зимой", "Иркутск", TourKind.EXCURSION,
                     date(2027, 2, 1), date(2027, 2, 8), 78000, ivanova))
    op.add_quota("T-001", "Отель «Волга»", 6)
    op.add_quota("T-001", "Автобус «Тур-Транс»", 4)
    op.publish("T-001")
    print("В продаже:", op.find_tours(max_price=50000))
    v1 = op.sell("T-001", "Петров Пётр", "4510 123456", 2, today=date(2026, 3, 1))
    v2 = op.sell("T-001", "Сидорова Мария", "4511 654321", 4, today=date(2026, 3, 2))
    print(f"{v1.number}: {v1.amount:.2f} ₽, {v1.pay(32000)}")
    print(f"{v2.number}: {v2.amount:.2f} ₽ (скидка 5 %), {v2.pay(v2.amount)}")
    print(f"Остаток мест: {ring.seats_left}, загрузка {ring.load_percent} %")
    ring.status = TourStatus.FINISHED
    op.leave_review(v1.number, 5, "Отличный гид!")
    op.leave_review(v2.number, 4)
    print("Средняя оценка:", op.avg_rating("T-001"))
    for row in op.load_report():
        print("  {:<16} {:>2}/{:<2} {:>5}%  {}".format(*row))
    print("Выручка:", op.revenue(), "₽")


if __name__ == "__main__":
    main()
