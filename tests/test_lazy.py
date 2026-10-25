import inspect

from core.domain import Order
from core.lazy import iter_orders_by_day, lazy_top_customers

ORDERS = (
    Order("o1", "u1", (), 1000, "2026-01-01", "paid"),
    Order("o2", "u2", (), 2000, "2026-01-01", "paid"),
    Order("o3", "u1", (), 500, "2026-01-02", "paid"),
    Order("o4", "u3", (), 9000, "2026-01-01", "refunded"),
)


def test_iter_orders_by_day_is_a_generator():
    result = iter_orders_by_day(ORDERS, "2026-01-01")
    assert inspect.isgenerator(result)


def test_iter_orders_by_day_yields_only_matching_day():
    result = tuple(iter_orders_by_day(ORDERS, "2026-01-01"))
    assert tuple(o.id for o in result) == ("o1", "o2", "o4")


def test_iter_orders_by_day_excludes_other_days():
    result = tuple(iter_orders_by_day(ORDERS, "2026-01-02"))
    assert tuple(o.id for o in result) == ("o3",)


def test_lazy_top_customers_is_a_generator():
    result = lazy_top_customers(ORDERS, k=10)
    assert inspect.isgenerator(result)


def test_lazy_top_customers_ranks_by_paid_spend_and_respects_k():
    result = tuple(lazy_top_customers(ORDERS, k=1))
    assert result == (("u2", 2000),)


def test_lazy_top_customers_ignores_non_paid_orders():
    result = dict(lazy_top_customers(ORDERS, k=10))
    assert "u3" not in result  # единственный заказ u3 — refunded
