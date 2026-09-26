"""Классы предметной области «Туроператор» (ПР №4).

Свойства (@property) с проверкой — аналог пары Property Get / Property Let
из примера методички на VB: чтение отдаёт значение, запись его проверяет.
"""
import re
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class TourStatus(Enum):
    DRAFT = "черновик"
    ON_SALE = "в продаже"
    SOLD_OUT = "распродан"
    RUNNING = "проводится"
    FINISHED = "завершён"
    CANCELLED = "отменён"


class TourKind(Enum):
    EXCURSION = "экскурсионный"
    BUSINESS = "деловой"
    BEACH = "пляжный"
    WELLNESS = "оздоровительный"


class Manager:
    def __init__(self, manager_id, full_name, phone):
        self.manager_id = manager_id
        self.full_name = full_name
        self.phone = phone

    def __repr__(self):
        return f"Manager({self.full_name})"


class Client:
    PASSPORT = re.compile(r"^\d{4} \d{6}$")

    def __init__(self, client_id, full_name, passport, phone=""):
        self.client_id = client_id
        self.full_name = full_name
        self.passport = passport
        self.phone = phone

    @property
    def passport(self):
        return self._passport

    @passport.setter
    def passport(self, value):
        if not self.PASSPORT.match(value):
            raise ValueError("паспорт должен иметь вид «1234 567890»")
        self._passport = value

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if len(value.split()) < 2:
            raise ValueError("укажите фамилию и инициалы/имя")
        self._full_name = value.strip()


@dataclass
class Quota:
    partner: str
    seats_total: int
    seats_left: int = field(init=False)

    def __post_init__(self):
        if self.seats_total <= 0:
            raise ValueError("квота должна быть положительной")
        self.seats_left = self.seats_total


class Tour:
    def __init__(self, tour_id, title, destination, kind, date_from, date_to, price, manager):
        self.tour_id = tour_id
        self.title = title
        self.destination = destination
        self.kind = kind
        self.set_dates(date_from, date_to)
        self.price = price
        self.manager = manager
        self.status = TourStatus.DRAFT
        self.quotas = []
        self.program = []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("цена тура должна быть больше нуля")
        self._price = float(value)

    def set_dates(self, date_from: date, date_to: date):
        if date_to < date_from:
            raise ValueError("дата окончания раньше даты начала")
        self.date_from, self.date_to = date_from, date_to

    @property
    def nights(self):
        return (self.date_to - self.date_from).days

    @property
    def seats_total(self):
        return sum(q.seats_total for q in self.quotas)

    @property
    def seats_left(self):
        return sum(q.seats_left for q in self.quotas)

    @property
    def load_percent(self):
        return 0.0 if not self.seats_total else round(
            100 * (self.seats_total - self.seats_left) / self.seats_total, 1)

    def take_seats(self, seats):
        """Списывает места из квот по порядку их бронирования."""
        if seats > self.seats_left:
            raise ValueError("недостаточно мест в квотах")
        for quota in self.quotas:
            used = min(quota.seats_left, seats)
            quota.seats_left -= used
            seats -= used
        if self.seats_left == 0:
            self.status = TourStatus.SOLD_OUT

    def return_seats(self, seats):
        for quota in reversed(self.quotas):
            back = min(quota.seats_total - quota.seats_left, seats)
            quota.seats_left += back
            seats -= back
        if self.status is TourStatus.SOLD_OUT and self.seats_left > 0:
            self.status = TourStatus.ON_SALE

    def __repr__(self):
        return f"Tour({self.tour_id}, {self.title!r}, {self.status.value})"


class Voucher:
    BULK_SEATS = 4
    BULK_DISCOUNT = 0.05

    def __init__(self, number, tour, client, seats):
        if seats <= 0:
            raise ValueError("число мест должно быть положительным")
        self.number = number
        self.tour = tour
        self.client = client
        self.seats = seats
        self.amount = self.calc_amount(tour.price, seats)
        self.paid = 0.0
        self.review = None

    @classmethod
    def calc_amount(cls, price, seats):
        total = price * seats
        if seats >= cls.BULK_SEATS:
            total *= 1 - cls.BULK_DISCOUNT
        return round(total, 2)

    @property
    def status(self):
        if self.paid == 0:
            return "не оплачена"
        return "оплачена" if self.paid >= self.amount else "частично оплачена"

    def pay(self, money):
        if money <= 0 or self.paid + money > self.amount:
            raise ValueError("некорректная сумма оплаты")
        self.paid = round(self.paid + money, 2)
        return self.status


@dataclass
class Review:
    voucher: Voucher
    rating: int
    text: str = ""

    def __post_init__(self):
        if not 1 <= self.rating <= 5:
            raise ValueError("оценка от 1 до 5")
