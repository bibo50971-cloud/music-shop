"""Доменные модели. Все иммутабельны (@dataclass(frozen=True))."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Category:
    id: str
    name: str
    parent_id: Optional[str] = None


@dataclass(frozen=True)
class Product:
    id: str
    title: str
    price: int
    category_id: str
    tags: Tuple[str, ...]


@dataclass(frozen=True)
class User:
    id: str
    name: str
    tier: str


@dataclass(frozen=True)
class Cart:
    id: str
    user_id: str
    items: Tuple[Tuple[str, int], ...] = ()


@dataclass(frozen=True)
class Order:
    id: str
    user_id: str
    items: Tuple[Tuple[str, int], ...]
    total: int
    ts: str
    status: str
