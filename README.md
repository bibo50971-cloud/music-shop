# Music Shop — Аналитика интернет-магазина (Лаба №1)

Streamlit-приложение музыкального интернет-магазина в функциональном стиле:
чистые функции, иммутабельные данные, HOF (`map`/`filter`/`reduce`).

## Запуск

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app/main.py
```

## Навигация (меню)

- **Overview** — витрина товаров, фильтр по категориям, корзина, оформление заказа, агрегаты.
- **Data** — просмотр исходных данных (категории/товары/пользователи/заказы) из `data/seed.json`.
- **Functional Core** — демонстрация чистых функций и иммутабельности.
- Pipelines / Async/FRP / Reports / Tests / About — заглушки, будут реализованы в следующих лабораторных.

## Что реализовано (Лаба №1)

- `core/domain.py` — иммутабельные модели: `Category`, `Product`, `User`, `Cart`, `Order`.
- `core/transforms.py` — чистые функции: `load_seed`, `add_to_cart`, `remove_from_cart`,
  `checkout`, `total_sales` (на `reduce`), `count_paid_orders`/`average_order_value` (на `filter`/`reduce`).
- `data/seed.json` — 111 товаров в 14 категориях, 35 пользователей, 60 заказов
  (генерируется скриптом `scripts/generate_seed.py`).
- `tests/test_transforms.py` — 8 тестов: проверка объёма данных, неизменности исходных
  структур при `add_to_cart`/`remove_from_cart`, корректность `checkout`/`total_sales`.

## Проверка качества

```powershell
pytest -q
ruff check .
black --check .
```

## Участники

- <впишите ФИО участников команды>
