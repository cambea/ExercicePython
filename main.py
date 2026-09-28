from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP


def calculate_total(cart: list[dict], rules: dict) -> float:
    """Total du panier : remise au volume (règle 1) puis pack 3 pour 2 (règle 2)."""
    tiers = sorted(rules.get("volume_discounts", {}).items(), reverse=True)
    bundles = rules.get("bundle_categories", ())

    qty_by_id = defaultdict(int)
    for item in cart:
        qty_by_id[item["id"]] += item["qty"]

    total = Decimal(0)
    lines_by_category = defaultdict(list)  # catégorie -> [(prix unitaire remisé, qty)]
    for item in cart:
        if item["qty"] < 0 or item["price"] < 0:
            raise ValueError(f"qty et price doivent être positifs : {item}")
        rate = next(
            (
                Decimal(str(r))
                for threshold, r in tiers
                if qty_by_id[item["id"]] >= threshold
            ),
            Decimal(0),
        )
        unit = Decimal(str(item["price"])) * (1 - rate)
        total += unit * item["qty"]
        if item["category"] in bundles:
            lines_by_category[item["category"]].append((unit, item["qty"]))

    # Tri par prix décroissant, groupes de 3 : le 3e de chaque groupe est offert.
    # Nb de multiples de 3 dans ]position, position + qty] = (position + qty) // 3 - position // 3.
    for lines in lines_by_category.values():
        position = 0
        for unit, qty in sorted(lines, reverse=True):
            total -= unit * ((position + qty) // 3 - position // 3)
            position += qty

    return float(total.quantize(Decimal("0.01"), ROUND_HALF_UP))


if __name__ == "__main__":
    rules = {"volume_discounts": {5: 0.10, 10: 0.20}, "bundle_categories": ["book"]}
    cart = [
        {"id": "A", "category": "book", "price": 10.0, "qty": 4},
        {"id": "B", "category": "book", "price": 15.0, "qty": 1},
        {"id": "C", "category": "tech", "price": 100.0, "qty": 1},
    ]
    total = calculate_total(cart, rules)
    print(f"Total : {total} EUR")
    assert total == 145.00
