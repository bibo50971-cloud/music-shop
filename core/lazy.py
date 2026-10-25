"""Ленивые генераторы: потоковая обработка заказов без полной материализации (Лаба №5)."""

from typing import Dict, Iterable, Iterator, Tuple

from core.domain import Order


def iter_orders_by_day(orders: Iterable[Order], day: str) -> Iterator[Order]:
    for order in orders:
        if order.ts == day:
            yield order


def lazy_top_customers(orders: Iterable[Order], k: int) -> Iterator[Tuple[str, int]]:
    spend_by_user_id: Dict[str, int] = {}
    for order in orders:
        if order.status != "paid":
            continue
        spend_by_user_id[order.user_id] = spend_by_user_id.get(order.user_id, 0) + order.total

    ranked_ids = sorted(spend_by_user_id, key=lambda uid: spend_by_user_id[uid], reverse=True)
    for user_id in ranked_ids[:k]:
        yield user_id, spend_by_user_id[user_id]
