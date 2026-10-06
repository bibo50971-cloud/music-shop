from core.domain import Category, Product
from core.recursion import (
    by_category,
    by_price_range,
    collect_products_recursive,
    flatten_categories,
)

CATEGORIES = (
    Category("cat_a", "A", None),
    Category("cat_b", "B", "cat_a"),
    Category("cat_c", "C", "cat_b"),
    Category("cat_d", "D", "cat_a"),
    Category("cat_e", "E", None),
)

PRODUCTS = (
    Product("p1", "Prod A", 1000, "cat_a", ("acoustic",)),
    Product("p2", "Prod B", 2000, "cat_b", ("electric",)),
    Product("p3", "Prod C", 3000, "cat_c", ("electric", "premium")),
    Product("p4", "Prod D", 4000, "cat_d", ()),
    Product("p5", "Prod E", 5000, "cat_e", ("acoustic",)),
)


def test_by_category_filters_products_matching_category():
    matches = tuple(filter(by_category("cat_b"), PRODUCTS))
    assert matches == (PRODUCTS[1],)


def test_by_price_range_filters_products_within_bounds_inclusive():
    matches = tuple(filter(by_price_range(2000, 4000), PRODUCTS))
    assert matches == (PRODUCTS[1], PRODUCTS[2], PRODUCTS[3])


def test_flatten_categories_returns_root_and_all_descendants_recursively():
    result = flatten_categories(CATEGORIES, "cat_a")
    assert tuple(c.id for c in result) == ("cat_a", "cat_b", "cat_c", "cat_d")


def test_flatten_categories_returns_empty_tuple_for_unknown_root():
    assert flatten_categories(CATEGORIES, "cat_unknown") == ()


def test_collect_products_recursive_gathers_products_from_whole_subtree():
    result = collect_products_recursive(CATEGORIES, PRODUCTS, "cat_a")
    assert tuple(p.id for p in result) == ("p1", "p2", "p3", "p4")
