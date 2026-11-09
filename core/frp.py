"""Шина событий магазина (FRP) и чистые подписчики-обработчики (Лаба №6)."""

from typing import Callable, Dict, List, NamedTuple


class Event(NamedTuple):
    name: str
    ts: str
    payload: dict


Handler = Callable[[Event, dict], dict]


class EventBus:
    def __init__(self, initial_state: dict):
        self._handlers: Dict[str, List[Handler]] = {}
        self._state = initial_state

    def subscribe(self, name: str, handler: Handler) -> None:
        self._handlers.setdefault(name, []).append(handler)

    def publish(self, name: str, payload: dict, ts: str = "") -> dict:
        event = Event(name=name, ts=ts, payload=payload)
        for handler in self._handlers.get(name, ()):
            self._state = handler(event, self._state)
        return self._state

    @property
    def state(self) -> dict:
        return self._state


def handle_add_to_cart(event: Event, state: dict) -> dict:
    user_id = event.payload["user_id"]
    product_id = event.payload["product_id"]
    qty = event.payload.get("qty", 1)

    carts = dict(state["carts"])
    user_cart = dict(carts.get(user_id, {}))
    user_cart[product_id] = user_cart.get(product_id, 0) + qty
    carts[user_id] = user_cart

    return {**state, "carts": carts}


def handle_remove(event: Event, state: dict) -> dict:
    user_id = event.payload["user_id"]
    product_id = event.payload["product_id"]

    carts = dict(state["carts"])
    user_cart = dict(carts.get(user_id, {}))
    user_cart.pop(product_id, None)
    carts[user_id] = user_cart

    return {**state, "carts": carts}


def handle_checkout(event: Event, state: dict) -> dict:
    user_id = event.payload["user_id"]
    amount = event.payload["amount"]

    carts = dict(state["carts"])
    carts[user_id] = {}

    return {**state, "carts": carts, "total_sales": state["total_sales"] + amount}


def handle_refund(event: Event, state: dict) -> dict:
    amount = event.payload["amount"]
    return {
        **state,
        "total_sales": state["total_sales"] - amount,
        "refunds": state["refunds"] + 1,
    }


def create_shop_event_bus() -> EventBus:
    bus = EventBus(initial_state={"carts": {}, "total_sales": 0, "refunds": 0})
    bus.subscribe("ADD_TO_CART", handle_add_to_cart)
    bus.subscribe("REMOVE", handle_remove)
    bus.subscribe("CHECKOUT", handle_checkout)
    bus.subscribe("REFUND", handle_refund)
    return bus
