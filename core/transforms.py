"""Чистые трансформации над доменными данными (Лаба №1: HOF, иммутабельность)."""

import json
from functools import reduce
from typing import Dict, Tuple

from core.domain import Cart, Category, Order, Product, User


def load_seed(
    path: str,
) -> Tuple[Tuple[Category, ...], Tuple[Product, ...], Tuple[User, ...], Tuple[Order, ...]]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    categories = tuple(Category(c["id"], c["name"], c.get("parent_id")) for c in raw["categories"])
    products = tuple(
        Product(p["id"], p["title"], p["price"], p["category_id"], tuple(p["tags"])) for p in raw["products"]
    )
    users = tuple(User(u["id"], u["name"], u["tier"]) for u in raw["users"])
    orders = tuple(
        Order(
            o["id"],
            o["user_id"],
            tuple((pid, qty) for pid, qty in o["items"]),
            o["total"],
            o["ts"],
            o["status"],
        )
        for o in raw["orders"]
    )
    return categories, products, users, orders


def add_to_cart(cart: Cart, product_id: str, qty: int) -> Cart:
    existing = dict(cart.items)
    existing[product_id] = existing.get(product_id, 0) + qty
    return Cart(id=cart.id, user_id=cart.user_id, items=tuple(existing.items()))


def remove_from_cart(cart: Cart, product_id: str) -> Cart:
    new_items = tuple(item for item in cart.items if item[0] != product_id)
    return Cart(id=cart.id, user_id=cart.user_id, items=new_items)


def checkout(cart: Cart, products: Tuple[Product, ...], order_id: str, ts: str) -> Order:
    price_by_id: Dict[str, int] = {p.id: p.price for p in products}
    line_totals = map(lambda item: price_by_id.get(item[0], 0) * item[1], cart.items)
    total = reduce(lambda acc, x: acc + x, line_totals, 0)
    return Order(id=order_id, user_id=cart.user_id, items=cart.items, total=total, ts=ts, status="paid")


def total_sales(orders: Tuple[Order, ...]) -> int:
    paid_orders = filter(lambda o: o.status == "paid", orders)
    return reduce(lambda acc, o: acc + o.total, paid_orders, 0)


def count_paid_orders(orders: Tuple[Order, ...]) -> int:
    return len(tuple(filter(lambda o: o.status == "paid", orders)))


def average_order_value(orders: Tuple[Order, ...]) -> float:
    paid_orders = tuple(filter(lambda o: o.status == "paid", orders))
    if not paid_orders:
        return 0.0
    return total_sales(paid_orders) / len(paid_orders)


def cart_line_items(cart: Cart, products: Tuple[Product, ...]) -> Tuple[Tuple[Product, int, int], ...]:
    price_by_id: Dict[str, Product] = {p.id: p for p in products}
    return tuple(
        (price_by_id[pid], qty, price_by_id[pid].price * qty) for pid, qty in cart.items if pid in price_by_id
    )
