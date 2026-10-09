"""Функциональные контейнеры Maybe/Either и операции на их основе (Лаба №4)."""

from dataclasses import dataclass
from typing import Callable, Dict, Generic, Optional, Tuple, TypeVar

from core.domain import Discount, Order, Product

T = TypeVar("T")
U = TypeVar("U")
L = TypeVar("L")
R = TypeVar("R")


@dataclass(frozen=True)
class Maybe(Generic[T]):
    _value: Optional[T]

    @staticmethod
    def some(value: T) -> "Maybe[T]":
        return Maybe(value)

    @staticmethod
    def nothing() -> "Maybe[T]":
        return Maybe(None)

    def is_some(self) -> bool:
        return self._value is not None

    def map(self, func: Callable[[T], U]) -> "Maybe[U]":
        if self._value is None:
            return Maybe.nothing()
        return Maybe.some(func(self._value))

    def bind(self, func: Callable[[T], "Maybe[U]"]) -> "Maybe[U]":
        if self._value is None:
            return Maybe.nothing()
        return func(self._value)

    def get_or_else(self, default: T) -> T:
        return self._value if self._value is not None else default


@dataclass(frozen=True)
class Either(Generic[L, R]):
    _left: Optional[L]
    _right: Optional[R]

    @staticmethod
    def left(value: L) -> "Either[L, R]":
        return Either(value, None)

    @staticmethod
    def right(value: R) -> "Either[L, R]":
        return Either(None, value)

    def is_right(self) -> bool:
        return self._right is not None

    def map(self, func: Callable[[R], U]) -> "Either[L, U]":
        if self._right is None:
            return Either.left(self._left)
        return Either.right(func(self._right))

    def bind(self, func: Callable[[R], "Either[L, U]"]) -> "Either[L, U]":
        if self._right is None:
            return Either.left(self._left)
        return func(self._right)

    def get_or_else(self, default: R) -> R:
        return self._right if self._right is not None else default

    def left_or_else(self, default: L) -> L:
        return self._left if self._left is not None else default


def safe_product(products: Tuple[Product, ...], pid: str) -> Maybe[Product]:
    found = next((p for p in products if p.id == pid), None)
    if found is None:
        return Maybe.nothing()
    return Maybe.some(found)


def validate_order(order: Order, stock: Dict[str, int], discounts: Tuple[Discount, ...]) -> Either[dict, Order]:
    for product_id, qty in order.items:
        available = stock.get(product_id, 0)
        if qty > available:
            return Either.left(
                {
                    "error": "out_of_stock",
                    "product_id": product_id,
                    "requested": qty,
                    "available": available,
                }
            )

    applicable = tuple(d for d in discounts if order.total >= d.conditions.get("min_total", 0))
    if not applicable:
        return Either.right(order)

    best = max(applicable, key=lambda d: d.percent)
    discounted_total = round(order.total * (100 - best.percent) / 100)
    discounted_order = Order(
        id=order.id,
        user_id=order.user_id,
        items=order.items,
        total=discounted_total,
        ts=order.ts,
        status=order.status,
    )
    return Either.right(discounted_order)
