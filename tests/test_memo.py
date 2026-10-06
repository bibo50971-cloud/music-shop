from core.domain import Order, Product, User
from core.memo import segment_customers, top_products

PRODUCTS = (
    Product("p1", "Guitar", 10000, "cat_a", ()),
    Product("p2", "Drum", 20000, "cat_b", ()),
    Product("p3", "Mic", 5000, "cat_c", ()),
)

ORDERS = (
    Order("o1", "u1", (("p1", 3),), 30000, "2026-01-01", "paid"),
    Order("o2", "u2", (("p2", 5),), 100000, "2026-01-02", "paid"),
    Order("o3", "u1", (("p2", 1),), 20000, "2026-01-03", "paid"),
    Order("o4", "u3", (("p3", 10),), 50000, "2026-01-04", "refunded"),
)

USERS = (
    User("u1", "Alice", "regular"),
    User("u2", "Bob", "vip"),
    User("u3", "Carl", "regular"),
)


def test_top_products_ranks_by_quantity_sold_in_paid_orders():
    top_products.cache_clear()
    result = top_products(ORDERS, PRODUCTS, k=10)
    assert tuple(p.id for p in result) == ("p2", "p1")


def test_top_products_respects_k_limit():
    top_products.cache_clear()
    result = top_products(ORDERS, PRODUCTS, k=1)
    assert tuple(p.id for p in result) == ("p2",)


def test_top_products_ignores_non_paid_orders():
    top_products.cache_clear()
    result = top_products(ORDERS, PRODUCTS, k=10)
    assert all(p.id != "p3" for p in result)  # p3 только в refunded-заказе


def test_top_products_uses_cache_on_repeated_calls():
    top_products.cache_clear()
    top_products(ORDERS, PRODUCTS, k=2)
    top_products(ORDERS, PRODUCTS, k=2)
    info = top_products.cache_info()
    assert info.hits == 1
    assert info.misses == 1


def test_segment_customers_classifies_by_total_paid_spend():
    segment_customers.cache_clear()
    result = dict(segment_customers(ORDERS, USERS))
    assert result["u2"] == "VIP"       # 100000 paid -> VIP
    assert result["u1"] == "regular"   # 30000+20000=50000 paid -> regular
    assert result["u3"] == "inactive"  # единственный заказ refunded -> 0 paid
