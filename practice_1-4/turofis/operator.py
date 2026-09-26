"""Сервисный класс TourOperator — точка входа для интерфейса (ПР №4)."""
import csv
from datetime import date

from .models import Client, Quota, Review, Tour, TourStatus, Voucher


class TourOperator:
    def __init__(self, name):
        self.name = name
        self.tours = {}
        self.clients = {}      # паспорт -> Client
        self.vouchers = []
        self._next_client = 1

    # --- туры ---
    def add_tour(self, tour: Tour):
        if tour.tour_id in self.tours:
            raise ValueError("тур с таким кодом уже есть")
        self.tours[tour.tour_id] = tour
        return tour

    def add_quota(self, tour_id, partner, seats):
        tour = self.tours[tour_id]
        tour.quotas.append(Quota(partner, seats))
        return tour.seats_left

    def publish(self, tour_id):
        tour = self.tours[tour_id]
        if tour.status is not TourStatus.DRAFT or tour.seats_left == 0:
            raise ValueError("опубликовать можно черновик с квотой мест")
        tour.status = TourStatus.ON_SALE

    def cancel(self, tour_id):
        self.tours[tour_id].status = TourStatus.CANCELLED

    def find_tours(self, destination=None, max_price=None, start_after=None):
        found = [t for t in self.tours.values() if t.status is TourStatus.ON_SALE]
        if destination:
            found = [t for t in found if destination.lower() in t.destination.lower()]
        if max_price is not None:
            found = [t for t in found if t.price <= max_price]
        if start_after is not None:
            found = [t for t in found if t.date_from >= start_after]
        return sorted(found, key=lambda t: (t.date_from, t.price))

    # --- продажи ---
    def client_by_passport(self, full_name, passport, phone=""):
        if passport not in self.clients:
            self.clients[passport] = Client(self._next_client, full_name, passport, phone)
            self._next_client += 1
        return self.clients[passport]

    def sell(self, tour_id, full_name, passport, seats, today=None):
        tour = self.tours.get(tour_id)
        if tour is None or tour.status is not TourStatus.ON_SALE:
            raise ValueError("тур недоступен для продажи")
        client = self.client_by_passport(full_name, passport)
        year = (today or date.today()).year
        voucher = Voucher(f"V-{year}-{len(self.vouchers) + 1:04d}", tour, client, seats)
        tour.take_seats(seats)
        self.vouchers.append(voucher)
        return voucher

    def refund(self, number):
        voucher = self._voucher(number)
        voucher.tour.return_seats(voucher.seats)
        self.vouchers.remove(voucher)

    def _voucher(self, number):
        for v in self.vouchers:
            if v.number == number:
                return v
        raise KeyError(number)

    def leave_review(self, number, rating, text=""):
        voucher = self._voucher(number)
        if voucher.tour.status is not TourStatus.FINISHED:
            raise ValueError("отзыв принимается после завершения тура")
        if voucher.review:
            raise ValueError("отзыв уже оставлен")
        voucher.review = Review(voucher, rating, text)
        return voucher.review

    # --- отчёты ---
    def load_report(self):
        rows = []
        for t in self.tours.values():
            mark = "высокая" if t.load_percent >= 80 else "нужна реклама"
            rows.append((t.title, t.seats_total - t.seats_left, t.seats_total, t.load_percent, mark))
        return rows

    def revenue(self):
        return round(sum(v.paid for v in self.vouchers), 2)

    def avg_rating(self, tour_id):
        marks = [v.review.rating for v in self.vouchers if v.tour.tour_id == tour_id and v.review]
        return round(sum(marks) / len(marks), 2) if marks else None

    def export_sales(self, path):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["Путёвка", "Тур", "Клиент", "Мест", "Сумма", "Оплачено", "Статус"])
            for v in self.vouchers:
                w.writerow([v.number, v.tour.title, v.client.full_name, v.seats, v.amount, v.paid, v.status])
        return len(self.vouchers)
