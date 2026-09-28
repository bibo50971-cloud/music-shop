"""Замыкания-фильтры и рекурсивный обход дерева категорий (Лаба №2)."""

from typing import Callable, Tuple

from core.domain import Category, Product, User


def by_category(cat_id: str) -> Callable[[Product], bool]:
    def predicate(product: Product) -> bool:
        return product.category_id == cat_id

    return predicate


def by_price_range(min_price: int, max_price: int) -> Callable[[Product], bool]:
    def predicate(product: Product) -> bool:
        return min_price <= product.price <= max_price

    return predicate


def by_tag(tag: str) -> Callable[[Product], bool]:
    def predicate(product: Product) -> bool:
        return tag in product.tags

    return predicate


def by_user_tier(tier: str) -> Callable[[User], bool]:
    def predicate(user: User) -> bool:
        return user.tier == tier

    return predicate


def flatten_categories(categories: Tuple[Category, ...], root: str) -> Tuple[Category, ...]:
    root_category = next((c for c in categories if c.id == root), None)
    if root_category is None:
        return ()

    children = tuple(c for c in categories if c.parent_id == root)
    descendants = tuple(
        descendant for child in children for descendant in flatten_categories(categories, child.id)
    )
    return (root_category,) + descendants


def collect_products_recursive(
    categories: Tuple[Category, ...], products: Tuple[Product, ...], root_id: str
) -> Tuple[Product, ...]:
    own_products = tuple(p for p in products if p.category_id == root_id)
    children = tuple(c for c in categories if c.parent_id == root_id)
    child_products = tuple(
        product
        for child in children
        for product in collect_products_recursive(categories, products, child.id)
    )
    return own_products + child_products
