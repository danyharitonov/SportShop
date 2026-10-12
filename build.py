"""Скрипт локальной сборки «СпортТовары»: python build.py [--run]"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
REQUIRED_FILES = ["main.py", "data/products.json", "src/__init__.py", "src/catalog.py",
                  "src/cart.py", "src/orders.py", "src/analytics.py", "src/storage.py"]


def step(n, text):
    print(f"[{n}/5] {text}")


def check_python_version():
    step(1, f"Python {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("  ✗ Требуется Python 3.10+")
        sys.exit(1)
    print("  ✓ версия подходит")


def check_structure():
    step(2, "Структура проекта")
    missing = [f for f in REQUIRED_FILES if not os.path.exists(os.path.join(ROOT, f))]
    if missing:
        print("  ✗ нет файлов:", ", ".join(missing))
        sys.exit(1)
    print(f"  ✓ все {len(REQUIRED_FILES)} файлов на месте")


def check_data():
    step(3, "Данные data/products.json")
    path = os.path.join(ROOT, "data", "products.json")
    if not os.path.exists(path):
        print("  ✗ Файл данных не найден!")
        sys.exit(1)
    try:
        with open(path, encoding="utf-8") as fh:
            products = json.load(fh)
    except json.JSONDecodeError as exc:
        print(f"  ✗ JSON повреждён: {exc}")
        sys.exit(1)
    print(f"  ✓ товаров в каталоге: {len(products)}")


def run_tests():
    step(4, "Тесты (unittest discover)")
    started = time.perf_counter()
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                            cwd=ROOT, capture_output=True, text=True)
    summary = [line for line in result.stderr.splitlines() if line.startswith(("Ran", "OK", "FAILED"))]
    print("  " + " | ".join(summary) + f"  ({time.perf_counter() - started:.1f} с)")
    if result.returncode != 0:
        print(result.stderr)
        print("  ✗ Тесты не прошли!")
        sys.exit(1)


def run_app(interactive=False):
    step(5, "Запуск приложения" + ("" if interactive else " (проверка старта)"))
    if interactive:
        subprocess.run([sys.executable, "main.py"], cwd=ROOT)
        return
    res = subprocess.run([sys.executable, "main.py"], cwd=ROOT, input="0\n",
                         capture_output=True, text=True, timeout=20)
    if res.returncode != 0 or "До свидания!" not in res.stdout:
        print(res.stderr)
        print("  ✗ Приложение не запускается")
        sys.exit(1)
    print("  ✓ main.py стартует, меню выводится, выход по «0»")


if __name__ == "__main__":
    check_python_version()
    check_structure()
    check_data()
    run_tests()
    run_app(interactive="--run" in sys.argv)
    print("Сборка успешна!")
