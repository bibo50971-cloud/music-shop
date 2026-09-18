"""Генератор фиктивных данных для data/seed.json (запускать один раз вручную)."""

import json
import random
from pathlib import Path

random.seed(42)

CATEGORIES = [
    ("cat_electric_guitars", "Электрогитары", None),
    ("cat_acoustic_guitars", "Акустические гитары", None),
    ("cat_bass", "Бас-гитары", None),
    ("cat_amps", "Комбоусилители", None),
    ("cat_drums", "Ударные установки", None),
    ("cat_keys", "Клавишные и синтезаторы", None),
    ("cat_mics", "Микрофоны", None),
    ("cat_cables", "Кабели", None),
    ("cat_pedals", "Педали эффектов", None),
    ("cat_strings", "Струны", None),
    ("cat_cases", "Чехлы и кейсы", None),
    ("cat_stands", "Стойки и держатели", None),
    ("cat_dj", "DJ-оборудование", None),
    ("cat_monitors", "Студийные мониторы", None),
]

BRANDS_BY_CAT = {
    "cat_electric_guitars": ["Fender", "Gibson", "Ibanez", "Yamaha", "ESP", "Squier", "PRS", "Jackson"],
    "cat_acoustic_guitars": ["Yamaha", "Taylor", "Martin", "Fender", "Cort", "Takamine"],
    "cat_bass": ["Fender", "Ibanez", "Music Man", "Yamaha", "Squier", "Sterling"],
    "cat_amps": ["Boss", "Marshall", "Fender", "Orange", "Vox", "Blackstar"],
    "cat_drums": ["Pearl", "Tama", "Yamaha", "DW", "Mapex", "Sonor"],
    "cat_keys": ["Yamaha", "Korg", "Roland", "Nord", "Casio", "Novation"],
    "cat_mics": ["Shure", "Rode", "AKG", "Audio-Technica", "Sennheiser"],
    "cat_cables": ["Ernie Ball", "Fender", "Planet Waves", "Cordial"],
    "cat_pedals": ["Boss", "MXR", "Ibanez", "TC Electronic", "Electro-Harmonix"],
    "cat_strings": ["Ernie Ball", "D'Addario", "Elixir", "Dunlop"],
    "cat_cases": ["Gator", "Fender", "SKB", "Rockcase"],
    "cat_stands": ["On-Stage", "Hercules", "K&M", "Quik Lok"],
    "cat_dj": ["Pioneer DJ", "Numark", "Denon DJ", "Behringer"],
    "cat_monitors": ["KRK", "Yamaha", "JBL", "Presonus", "Adam Audio"],
}

MODELS_BY_CAT = {
    "cat_electric_guitars": ["Stratocaster", "Telecaster", "Les Paul", "SG", "RG550", "Explorer"],
    "cat_acoustic_guitars": ["Dreadnought", "GS Mini", "FG800", "Grand Auditorium", "Concert"],
    "cat_bass": ["Precision Bass", "Jazz Bass", "GSR200", "StingRay", "TRBX304"],
    "cat_amps": ["Katana-50", "DSL40CR", "Blues Junior", "Crush 20", "AC15"],
    "cat_drums": ["Export", "Superstar", "Stage Custom", "Performer", "Force"],
    "cat_keys": ["PSR-E373", "Minilogue", "Juno-DS", "Electro", "CT-S300"],
    "cat_mics": ["SM58", "NT1", "C214", "AT2020", "e935"],
    "cat_cables": ["Instrument Cable 6m", "Patch Cable", "XLR Cable 3m"],
    "cat_pedals": ["DS-1", "Phase 90", "Tube Screamer", "Ditto Looper", "Big Muff"],
    "cat_strings": ["Regular Slinky", "XL Nickel", "Optiweb", "Phosphor Bronze"],
    "cat_cases": ["Gig Bag", "Hardshell Case", "Flight Case"],
    "cat_stands": ["Guitar Stand", "Mic Stand", "Keyboard Stand", "Amp Stand"],
    "cat_dj": ["DDJ-400", "Mixtrack Pro", "SC5000", "CMD Studio 4a"],
    "cat_monitors": ["Rokit 5", "HS5", "305P MkII", "Eris E5"],
}

PRICE_RANGES = {
    "cat_electric_guitars": (120000, 750000),
    "cat_acoustic_guitars": (80000, 500000),
    "cat_bass": (100000, 600000),
    "cat_amps": (60000, 350000),
    "cat_drums": (250000, 1200000),
    "cat_keys": (70000, 900000),
    "cat_mics": (15000, 250000),
    "cat_cables": (3000, 15000),
    "cat_pedals": (20000, 90000),
    "cat_strings": (2500, 9000),
    "cat_cases": (10000, 60000),
    "cat_stands": (5000, 25000),
    "cat_dj": (150000, 800000),
    "cat_monitors": (40000, 300000),
}


def gen_products():
    products = []
    idx = 1
    for cat_id, _, _ in CATEGORIES:
        brands = BRANDS_BY_CAT[cat_id]
        models = MODELS_BY_CAT[cat_id]
        lo, hi = PRICE_RANGES[cat_id]
        count = random.randint(7, 9)
        for _ in range(count):
            brand = random.choice(brands)
            model = random.choice(models)
            price = round(random.randint(lo, hi), -2)
            tags = tuple(
                sorted(
                    {brand.lower().replace(" ", "-"), cat_id.replace("cat_", ""), model.lower().split()[0]}
                )
            )
            products.append(
                {
                    "id": f"prod_{idx}",
                    "title": f"{brand} {model}",
                    "price": price,
                    "category_id": cat_id,
                    "tags": list(tags),
                }
            )
            idx += 1
    return products


FIRST_NAMES = [
    "Алия",
    "Данияр",
    "Ержан",
    "Айгерим",
    "Нурлан",
    "Диана",
    "Тимур",
    "Сабина",
    "Асхат",
    "Жанна",
    "Марат",
    "Гульнара",
    "Бекзат",
    "Мадина",
    "Санжар",
    "Айдана",
    "Руслан",
    "Дана",
    "Олжас",
    "Камила",
]
LAST_NAMES = [
    "Ахметов",
    "Сериков",
    "Жумабаев",
    "Токтаров",
    "Абенов",
    "Касымов",
    "Оспанов",
    "Нурлыбаев",
    "Сатыбалдин",
    "Ибрагимов",
]


def gen_users(n=35):
    users = []
    for i in range(1, n + 1):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        tier = "vip" if random.random() < 0.2 else "regular"
        users.append({"id": f"usr_{i}", "name": name, "tier": tier})
    return users


def gen_orders(products, users, n=60):
    orders = []
    statuses = ["paid"] * 7 + ["refunded"] * 2 + ["cancelled"] * 1
    for i in range(1, n + 1):
        user = random.choice(users)
        item_count = random.randint(1, 4)
        chosen = random.sample(products, item_count)
        items = [[p["id"], random.randint(1, 3)] for p in chosen]
        total = sum(next(p for p in products if p["id"] == pid)["price"] * qty for pid, qty in items)
        month = random.randint(1, 9)
        day = random.randint(1, 28)
        ts = f"2026-{month:02d}-{day:02d}"
        status = random.choice(statuses)
        orders.append(
            {
                "id": f"ord_{i}",
                "user_id": user["id"],
                "items": items,
                "total": total,
                "ts": ts,
                "status": status,
            }
        )
    return orders


def main():
    products = gen_products()
    users = gen_users()
    orders = gen_orders(products, users)
    data = {
        "categories": [{"id": c[0], "name": c[1], "parent_id": c[2]} for c in CATEGORIES],
        "products": products,
        "users": users,
        "orders": orders,
    }
    out_path = Path(__file__).resolve().parent.parent / "data" / "seed.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Готово: {len(products)} товаров, {len(users)} пользователей, {len(orders)} заказов -> {out_path}")


if __name__ == "__main__":
    main()
