from pathlib import Path

from core.domain import Cart, Order
from core.transforms import (
    add_to_cart,
    average_order_value,
    cart_line_items,
    checkout,
    count_paid_orders,
    load_seed,
    remove_from_cart,
    total_sales,
)

SEED_PATH = str(Path(__file__).resolve().parent.parent / "data" / "seed.json")


def test_load_seed_returns_expected_volumes():
    categories, products, users, orders = load_seed(SEED_PATH)
    assert len(products) >= 100
    assert 10 <= len(categories) <= 15
    assert len(users) >= 30
    assert len(orders) >= 50


def test_add_to_cart_does_not_mutate_original_cart():
    cart = Cart(id="c1", user_id="u1", items=(("prod_1", 1),))
    new_cart = add_to_cart(cart, "prod_1", 2)

    assert cart.items == (("prod_1", 1),)  # исходная корзина не изменилась
    assert dict(new_cart.items)["prod_1"] == 3


def test_add_to_cart_new_product_is_appended():
    cart = Cart(id="c1", user_id="u1", items=())
    new_cart = add_to_cart(cart, "prod_5", 1)
    assert dict(new_cart.items) == {"prod_5": 1}


def test_remove_from_cart_returns_new_cart_without_item():
    cart = Cart(id="c1", user_id="u1", items=(("prod_1", 1), ("prod_2", 3)))
    new_cart = remove_from_cart(cart, "prod_1")

    assert cart.items == (("prod_1", 1), ("prod_2", 3))  # исходная корзина не изменилась
    assert dict(new_cart.items) == {"prod_2": 3}


def test_total_sales_sums_only_paid_orders():
    orders = (
        Order("o1", "u1", (("prod_1", 1),), 1000, "2026-01-01", "paid"),
        Order("o2", "u1", (("prod_2", 1),), 500, "2026-01-02", "refunded"),
        Order("o3", "u2", (("prod_1", 2),), 2000, "2026-01-03", "paid"),
    )
    assert total_sales(orders) == 3000


def test_count_paid_orders_and_average_order_value():
    orders = (
        Order("o1", "u1", (), 1000, "2026-01-01", "paid"),
        Order("o2", "u1", (), 3000, "2026-01-02", "paid"),
        Order("o3", "u2", (), 999, "2026-01-03", "cancelled"),
    )
    assert count_paid_orders(orders) == 2
    assert average_order_value(orders) == 2000.0


def test_checkout_computes_total_from_product_prices():
    _, products, _, _ = load_seed(SEED_PATH)
    prod = products[0]
    cart = Cart(id="c1", user_id="usr_1", items=((prod.id, 2),))

    order = checkout(cart, products, order_id="ord_test", ts="2026-09-18")

    assert isinstance(order, Order)
    assert order.total == prod.price * 2
    assert order.status == "paid"
    assert order.items == cart.items  # сам заказ не переиспользует изменяемое состояние корзины


def test_cart_line_items_matches_products_and_quantities():
    _, products, _, _ = load_seed(SEED_PATH)
    p1, p2 = products[0], products[1]
    cart = Cart(id="c1", user_id="usr_1", items=((p1.id, 2), (p2.id, 1)))

    lines = cart_line_items(cart, products)

    assert len(lines) == 2
    line_by_id = {product.id: (qty, subtotal) for product, qty, subtotal in lines}
    assert line_by_id[p1.id] == (2, p1.price * 2)
    assert line_by_id[p2.id] == (1, p2.price * 1)
