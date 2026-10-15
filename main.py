"""СпортТовары — консольное приложение (точка входа)."""
from src.analytics import average_order_total, best_selling_product, total_revenue
from src.cart import add_to_cart, cart_total, remove_from_cart, update_quantity
from src.catalog import count_by_category, get_low_stock, search_advanced, stock_of
from src.orders import create_order, format_order, load_orders, save_orders
from src.storage import load_products, save_products

PRODUCTS_FILE = "data/products.json"
ORDERS_FILE = "data/orders.json"

MENU = """
──────── СпортТовары ────────
 1. Каталог
 2. Поиск товара
 3. Товары с низким остатком
 4. Добавить в корзину
 5. Корзина: показать / изменить / удалить
 6. Оформить заказ
 7. Аналитика продаж
 8. История заказов
 0. Выход"""


def ask(prompt, cast=str, default=None):
    """Ввод с преобразованием типа; пустая строка → default, ошибка → повтор."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return cast(raw)
        except ValueError:
            print("  Неверный ввод, попробуйте ещё раз.")


def print_products(products):
    if not products:
        print("  Ничего не найдено.")
    for p in products:
        sizes = ", ".join(f"{s}:{q}" for s, q in p["sizes"].items() if q > 0) or "нет в наличии"
        print(f"  {p['id']:>2}. {p['name']:<30} {p['category']:<10} {p['price']:>8.2f} ₽  [{sizes}]")


def show_cart(cart):
    if not cart:
        return print("  Корзина пуста.")
    for n, it in enumerate(cart, 1):
        print(f"  {n}) {it['name']:<30} р.{it['size']:<4} {it['qty']} × {it['price']:.2f}")
    print(f"  Итого со скидкой: {cart_total(cart):.2f} ₽")


def menu_search(products):
    query = ask("  Часть названия (Enter — любая): ", default="")
    category = ask("  Категория (Enter — любая): ", default="") or None
    lo = ask("  Цена от (Enter — без ограничения): ", float, default=-1.0)
    hi = ask("  Цена до (Enter — без ограничения): ", float, default=-1.0)
    print_products(search_advanced(products, query, category,
                                   None if lo < 0 else lo, None if hi < 0 else hi))


def menu_cart(cart, products):
    show_cart(cart)
    if not cart:
        return
    action = ask("  [и]зменить количество, [у]далить, Enter — назад: ", default="").lower()
    if action not in ("и", "у"):
        return
    n = ask("  Номер позиции: ", int)
    if not 1 <= n <= len(cart):
        return print("  Нет такой позиции.")
    it = cart[n - 1]
    if action == "у":
        remove_from_cart(cart, it["product_id"], it["size"])
        print("  Позиция удалена.")
    else:
        print(" ", update_quantity(cart, products, it["product_id"], it["size"], ask("  Новое количество: ", int))[1])


def menu_analytics(products, orders):
    print(f"  Заказов: {len(orders)}, выручка: {total_revenue(orders):.2f} ₽, "
          f"средний чек: {average_order_total(orders):.2f} ₽")
    best = best_selling_product(orders)
    print(f"  Хит продаж: {best[0]} ({best[1]} шт.)" if best else "  Хит продаж: пока нет продаж")
    print("  Наименований по категориям:", count_by_category(products))


def main():
    products = load_products(PRODUCTS_FILE)
    orders = load_orders(ORDERS_FILE)
    cart = []
    while True:
        print(MENU)
        choice = ask("Выберите пункт: ", default="")
        if choice == "1":
            print_products(products)
        elif choice == "2":
            menu_search(products)
        elif choice == "3":
            low = get_low_stock(products)
            for p in low:
                print(f"  ⚠ {p['name']} — осталось {stock_of(p)} шт.")
            if not low:
                print("  Все товары в достатке.")
        elif choice == "4":
            ok, msg = add_to_cart(cart, products, ask("  ID товара: ", int),
                                  ask("  Размер: ", int), ask("  Количество: ", int))
            print(" ", msg)
        elif choice == "5":
            menu_cart(cart, products)
        elif choice == "6":
            order = create_order(cart, ask("  Имя клиента: "), products)
            if order is None:
                print("  Корзина пуста или не указано имя.")
                continue
            orders.append(order)
            save_orders(orders, ORDERS_FILE)
            save_products(products, PRODUCTS_FILE)
            print(format_order(order))
            print(f"  Заказ сохранён в {ORDERS_FILE}")
        elif choice == "7":
            menu_analytics(products, orders)
        elif choice == "8":
            orders = load_orders(ORDERS_FILE)
            for o in orders:
                print(f"  {o['number']}  {o['date']}  {o['client']:<16} {o['total']:>10.2f} ₽")
            if not orders:
                print("  Заказов пока нет.")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("  Нет такого пункта меню.")


if __name__ == "__main__":
    main()
