from core.frp import Event, create_shop_event_bus, handle_add_to_cart

EMPTY_STATE = {"carts": {}, "total_sales": 0, "refunds": 0}


def test_add_to_cart_event_updates_live_cart():
    bus = create_shop_event_bus()
    state = bus.publish("ADD_TO_CART", {"user_id": "u1", "product_id": "p1", "qty": 2})
    assert state["carts"]["u1"] == {"p1": 2}


def test_remove_event_removes_product_from_cart():
    bus = create_shop_event_bus()
    bus.publish("ADD_TO_CART", {"user_id": "u1", "product_id": "p1", "qty": 2})
    state = bus.publish("REMOVE", {"user_id": "u1", "product_id": "p1"})
    assert "p1" not in state["carts"]["u1"]


def test_checkout_event_clears_cart_and_increases_sales():
    bus = create_shop_event_bus()
    bus.publish("ADD_TO_CART", {"user_id": "u1", "product_id": "p1", "qty": 1})
    state = bus.publish("CHECKOUT", {"user_id": "u1", "amount": 5000})
    assert state["carts"]["u1"] == {}
    assert state["total_sales"] == 5000


def test_refund_event_decreases_sales_and_counts_refund():
    bus = create_shop_event_bus()
    bus.publish("CHECKOUT", {"user_id": "u1", "amount": 5000})
    state = bus.publish("REFUND", {"amount": 2000})
    assert state["total_sales"] == 3000
    assert state["refunds"] == 1


def test_handlers_do_not_mutate_input_state():
    event = Event("ADD_TO_CART", "2026-01-01", {"user_id": "u1", "product_id": "p1", "qty": 1})
    original_carts = EMPTY_STATE["carts"]

    handle_add_to_cart(event, EMPTY_STATE)

    assert EMPTY_STATE["carts"] is original_carts
    assert EMPTY_STATE["carts"] == {}  # исходное состояние не изменилось


def test_unknown_event_name_leaves_state_unchanged():
    bus = create_shop_event_bus()
    state = bus.publish("UNKNOWN_EVENT", {})
    assert state == EMPTY_STATE
