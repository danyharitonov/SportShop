"""Практическая работа №5. Основы Python. Предметная область «Чудо Обувь».

Каждое задание методички оформлено отдельной функцией task_N(),
запуск всех заданий: python pr05_ChudoObuv/main.py
"""


def title(text):
    print(f"\n=== {text} ===")


# ---------- Задание 1. Первая программа ----------
def task_1():
    title("Задание 1. Первая программа")
    print("Привет! Это магазин «Чудо Обувь».")


# ---------- Задание 2. Переменные, print, for, if ----------
def task_2():
    title("Задание 2. Переменные, циклы, условие")
    model = "Gel-Kayano 30"     # str
    price = 13490.0             # float
    quantity = 5                # int
    in_stock = quantity > 0     # bool
    print(f"Модель: {model}; цена {price} руб.; остаток {quantity}; в наличии: {in_stock}")
    for brand in ["Asics", "Mizuno", "Saucony"]:
        print("  бренд:", brand)
    for size in range(38, 43):
        print(f"  размер {size}", end=";")
    print()
    for q in (quantity, 2):
        print("  Достаточно на складе" if q > 3 else "  Мало на складе", f"(количество {q})")


# ---------- Задание 3. Списки и словари ----------
USERS = [
    {"login": "admin", "role": "Администратор", "name": "Орлова Е.В."},
    {"login": "seller1", "role": "Продавец", "name": "Ким Д.А."},
    {"login": "client7", "role": "Клиент", "name": "Лебедев С.И."},
]

CATALOG = [
    {"id": 101, "name": "Gel-Kayano 30", "brand": "Asics", "price": 13490.0, "sizes": {40: 2, 41: 3, 42: 1}},
    {"id": 102, "name": "Wave Rider 27", "brand": "Mizuno", "price": 11990.0, "sizes": {39: 4, 41: 0}},
    {"id": 103, "name": "Ride 17", "brand": "Saucony", "price": 9790.0, "sizes": {42: 1}},
    {"id": 104, "name": "Кеды Classic", "brand": "Два мяча", "price": 3290.0, "sizes": {37: 6, 38: 5}},
]


def task_3():
    title("Задание 3. Списки и словари")
    for u in USERS:
        print(f"  {u['login']:<8} {u['role']:<14} {u['name']}")
    for p in CATALOG:
        print(f"  #{p['id']} {p['name']:<14} {p['price']:>8.0f} руб.  всего пар: {sum(p['sizes'].values())}")


# ---------- Задание 4. Функции ----------
def find_user(login):
    for u in USERS:
        if u["login"] == login:
            return u
    return None


def total_cost(items):
    """Сумма позиций вида {'price': ..., 'quantity': ...}."""
    return sum(it["price"] * it["quantity"] for it in items)


def task_4():
    title("Задание 4. Функции")
    print("  find_user('seller1') ->", find_user("seller1"))
    print("  find_user('ghost')   ->", find_user("ghost"))
    print("  total_cost ->", total_cost([{"price": 3290, "quantity": 2}, {"price": 9790, "quantity": 1}]))


# ---------- Задание 5. Сортировка и фильтрация ----------
def pairs(p):
    return sum(p["sizes"].values())


def task_5():
    title("Задание 5. Сортировка и фильтрация")
    for p in sorted(CATALOG, key=lambda p: p["price"]):
        print(f"  {p['price']:>8.0f}  {p['name']}")
    low = [p["name"] for p in CATALOG if pairs(p) <= 3]
    print("  Мало на складе (≤ 3):", low)


# ---------- Задание 6. Поиск по каталогу ----------
def search_by_name(text):
    return [p for p in CATALOG if text.lower() in p["name"].lower()]


def filter_by_price(lo, hi):
    return [p for p in CATALOG if lo <= p["price"] <= hi]


def task_6():
    title("Задание 6. Поиск")
    print("  'ride' ->", [p["name"] for p in search_by_name("ride")])
    print("  9000..12000 ->", [p["name"] for p in filter_by_price(9000, 12000)])


# ---------- Задание 7. Мини-задача «Корзина» ----------
def task_7():
    title("Задание 7. Корзина")
    basket = []

    def put(product_id, size, qty):
        product = next((p for p in CATALOG if p["id"] == product_id), None)
        if product is None:
            return print(f"  товар {product_id} не найден")
        if product["sizes"].get(size, 0) < qty:
            return print(f"  {product['name']} р.{size}: нет {qty} пар")
        basket.append({"name": product["name"], "size": size, "price": product["price"], "quantity": qty})
        print(f"  + {product['name']} р.{size} × {qty}")

    put(101, 41, 2)
    put(104, 38, 1)
    put(103, 44, 1)
    put(999, 40, 1)
    print(f"  Позиций: {len(basket)}, итого: {total_cost(basket):.2f} руб.")


# ---------- Задание 8. Самостоятельно ----------
def get_sizes(product):
    return sorted(size for size, qty in product["sizes"].items() if qty > 0)


def get_total_quantity(product):
    return sum(product["sizes"].values())


def task_8():
    title("Задание 8. Самостоятельно")
    CATALOG.append({"id": 105, "name": "Сандалии Trek", "brand": "Teva", "price": 5490.0, "sizes": {40: 3, 43: 2}})
    CATALOG.append({"id": 106, "name": "Бутсы Pro", "brand": "Kelme", "price": 6990.0, "sizes": {41: 1, 42: 2, 44: 1}})
    for p in CATALOG:
        print(f"  {p['name']:<14} размеры {get_sizes(p)}  всего {get_total_quantity(p)}")
    print("  По алфавиту:", [p["name"] for p in sorted(CATALOG, key=lambda p: p["name"])])
    print("  Дешевле 6000:", [p["name"] for p in CATALOG if p["price"] < 6000])
    queue = list(CATALOG)
    while queue:
        print("  while ->", queue.pop(0)["name"])


# ---------- Дополнительное задание ----------
ORDERS = [
    {"date": "2026-09-03", "client": "Лебедев С.И.", "items": [{"price": 3290, "quantity": 2}]},
    {"date": "2026-09-01", "client": "Ким Д.А.", "items": [{"price": 13490, "quantity": 1}, {"price": 5490, "quantity": 1}]},
    {"date": "2026-09-02", "client": "Орлова Е.В.", "items": [{"price": 9790, "quantity": 1}]},
]


def task_extra():
    title("Дополнительное задание. Заказы")
    for order in sorted(ORDERS, key=lambda o: o["date"]):
        print(f"  {order['date']}  {order['client']:<14} {total_cost(order['items']):>9.2f} руб.")


if __name__ == "__main__":
    for task in (task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8, task_extra):
        task()
