"""Кэш "дорогих" аналитических функций через functools.lru_cache (Лаба №3)."""

import time
from functools import lru_cache
from typing import Callable, Tuple

from core.domain import Order, Product, User


@lru_cache(maxsize=32)
def top_products(orders: Tuple[Order, ...], products: Tuple[Product, ...], k: int = 10) -> Tuple[Product, ...]:
    quantity_by_product_id: dict = {}
    for order in orders:
        if order.status != "paid":
            continue
        for product_id, qty in order.items:
            quantity_by_product_id[product_id] = quantity_by_product_id.get(product_id, 0) + qty

    product_by_id = {p.id: p for p in products}
    ranked_ids = sorted(quantity_by_product_id, key=lambda pid: quantity_by_product_id[pid], reverse=True)

    return tuple(product_by_id[pid] for pid in ranked_ids[:k] if pid in product_by_id)


@lru_cache(maxsize=32)
def segment_customers(orders: Tuple[Order, ...], users: Tuple[User, ...]) -> Tuple[Tuple[str, str], ...]:
    spend_by_user_id: dict = {}
    for order in orders:
        if order.status != "paid":
            continue
        spend_by_user_id[order.user_id] = spend_by_user_id.get(order.user_id, 0) + order.total

    def classify(total_spend: int) -> str:
        if total_spend >= 100_000:
            return "VIP"
        if total_spend > 0:
            return "regular"
        return "inactive"

    return tuple((user.id, classify(spend_by_user_id.get(user.id, 0))) for user in users)


def timed_call(func: Callable, *args, **kwargs) -> Tuple[object, float]:
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms
