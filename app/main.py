import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from core.domain import Cart
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

st.set_page_config(page_title="Музыкальный Интернет-Магазин", layout="wide")

categories, products, users, orders = load_seed(SEED_PATH)

if "cart" not in st.session_state:
    st.session_state.cart = Cart(id="cart_1", user_id="usr_1", items=())
if "orders" not in st.session_state:
    st.session_state.orders = orders

st.sidebar.title("🎵 Music Shop")
menu = st.sidebar.radio(
    "Навигация",
    ["Overview", "Data", "Functional Core", "Pipelines", "Async/FRP", "Reports", "Tests", "About"],
)

if menu == "Overview":
    st.title("🎸 Каталог музыкальных инструментов и аксессуаров")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Всего товаров", len(products))
    col2.metric("Категорий", len(categories))
    col3.metric("Пользователей", len(users))
    col4.metric("Общие продажи", f"{total_sales(st.session_state.orders):,} ₸")

    col5, col6 = st.columns(2)
    col5.metric("Оплаченных заказов", count_paid_orders(st.session_state.orders))
    col6.metric("Средний чек", f"{average_order_value(st.session_state.orders):,.0f} ₸")

    st.divider()
    st.subheader("Витрина товаров")

    cat_names = {c.id: c.name for c in categories}
    cat_filter = st.selectbox("Фильтр по категории", ["Все"] + [c.name for c in categories])
    visible_products = (
        products
        if cat_filter == "Все"
        else tuple(p for p in products if cat_names.get(p.category_id) == cat_filter)
    )

    cols = st.columns(3)
    for idx, prod in enumerate(visible_products):
        with cols[idx % 3]:
            st.markdown(f"**{prod.title}**")
            st.caption(cat_names.get(prod.category_id, prod.category_id))
            st.write(f"Цена: {prod.price:,} ₸")
            if st.button("В корзину 🛒", key=f"add_{prod.id}"):
                st.session_state.cart = add_to_cart(st.session_state.cart, prod.id, 1)
                st.success(f"Добавлено: {prod.title}")

    st.divider()
    st.subheader("🛒 Ваша корзина")
    line_items = cart_line_items(st.session_state.cart, products)
    if not line_items:
        st.info("Корзина пуста")
    else:
        cart_total = 0
        for product, qty, subtotal in line_items:
            cart_total += subtotal
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{product.title}** (x{qty})")
            c2.write(f"{subtotal:,} ₸")
            if c3.button("Удалить", key=f"del_{product.id}"):
                st.session_state.cart = remove_from_cart(st.session_state.cart, product.id)
                st.rerun()
        st.markdown(f"### Итого к оплате: {cart_total:,} ₸")
        if st.button("Оформить заказ ✅"):
            new_order = checkout(
                st.session_state.cart,
                products,
                order_id=f"ord_ui_{len(st.session_state.orders) + 1}",
                ts="2026-09-18",
            )
            st.session_state.orders = st.session_state.orders + (new_order,)
            st.session_state.cart = Cart(
                id=st.session_state.cart.id, user_id=st.session_state.cart.user_id, items=()
            )
            st.success(f"Заказ {new_order.id} оформлен на сумму {new_order.total:,} ₸")
            st.rerun()

elif menu == "Data":
    st.title("📂 Исходные данные (Data)")
    st.write(
        f"Товаров: {len(products)} · Категорий: {len(categories)} · "
        f"Пользователей: {len(users)} · Заказов: {len(st.session_state.orders)}"
    )
    tab1, tab2, tab3, tab4 = st.tabs(["Categories", "Products", "Users", "Orders"])
    with tab1:
        st.json([c.__dict__ for c in categories])
    with tab2:
        st.json([p.__dict__ for p in products])
    with tab3:
        st.json([u.__dict__ for u in users])
    with tab4:
        st.json([o.__dict__ for o in st.session_state.orders])

elif menu == "Functional Core":
    st.title("🧩 Functional Core")
    st.markdown(
        "Демонстрация чистых функций и HOF из `core/transforms.py`: "
        "`add_to_cart`, `remove_from_cart`, `checkout`, `total_sales` "
        "(построены на `map`/`filter`/`reduce`, не мутируют входные данные)."
    )
    st.code(
        "def total_sales(orders):\n"
        "    paid_orders = filter(lambda o: o.status == 'paid', orders)\n"
        "    return reduce(lambda acc, o: acc + o.total, paid_orders, 0)",
        language="python",
    )
    st.write("Проверка иммутабельности: `add_to_cart` возвращает новый объект `Cart`, исходный не меняется.")
    demo_cart = Cart(id="demo", user_id="usr_1", items=())
    demo_cart2 = add_to_cart(demo_cart, products[0].id, 2)
    col1, col2 = st.columns(2)
    col1.write("До:")
    col1.json(demo_cart.__dict__)
    col2.write("После:")
    col2.json({"id": demo_cart2.id, "user_id": demo_cart2.user_id, "items": list(demo_cart2.items)})

else:
    st.title(f"Раздел: {menu}")
    st.info("Раздел появится в следующих лабораторных работах.")
