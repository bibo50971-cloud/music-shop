from core.domain import Discount, Order, Product
from core.ftypes import Maybe, safe_product, validate_order

PRODUCTS = (
    Product("p1", "Guitar", 10000, "cat_a", ()),
    Product("p2", "Drum", 20000, "cat_b", ()),
)


def test_maybe_map_and_get_or_else_on_some():
    result = Maybe.some(5).map(lambda x: x * 2).get_or_else(0)
    assert result == 10


def test_maybe_map_short_circuits_on_nothing():
    result = Maybe.nothing().map(lambda x: x * 2).get_or_else(0)
    assert result == 0


def test_safe_product_returns_some_when_found_and_nothing_when_missing():
    found = safe_product(PRODUCTS, "p1")
    missing = safe_product(PRODUCTS, "unknown")

    assert found.get_or_else(None) == PRODUCTS[0]
    assert missing.get_or_else(None) is None


def test_validate_order_returns_left_when_stock_insufficient():
    order = Order("o1", "u1", (("p1", 5),), 50000, "2026-01-01", "paid")
    result = validate_order(order, stock={"p1": 2}, discounts=())

    assert not result.is_right()
    assert result.get_or_else("fallback") == "fallback"
    assert result.map(lambda o: o.total).get_or_else("fallback") == "fallback"  # map не выполняется при Left


def test_either_left_or_else_returns_error_payload_on_left():
    order = Order("o1", "u1", (("p1", 5),), 50000, "2026-01-01", "paid")
    result = validate_order(order, stock={"p1": 2}, discounts=())

    error = result.left_or_else({})
    assert error["error"] == "out_of_stock"
    assert error["product_id"] == "p1"
    assert result.left_or_else({}) != {}  # на Right left_or_else вернул бы default


def test_validate_order_applies_best_matching_discount():
    order = Order("o1", "u1", (("p1", 2),), 20000, "2026-01-01", "paid")
    discounts = (
        Discount("d1", "SALE10", 10, {"min_total": 10000}),
        Discount("d2", "SALE20", 20, {"min_total": 15000}),
    )

    result = validate_order(order, stock={"p1": 10}, discounts=discounts)

    assert result.is_right()
    assert result.map(lambda o: o.total).get_or_else(None) == 16000  # 20000 * (100-20)/100
