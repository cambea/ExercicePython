# calculate_total

`calculate_total(cart, rules) -> float` dans `main.py`. Stdlib uniquement.

- Lancer l'exemple :
  - macOS/Linux : `python3 main.py`
  - Windows : `python main.py`
- Lancer les tests (depuis la racine du projet) :
  - macOS/Linux : `python3 -m unittest discover -s tests`
  - Windows : `python -m unittest discover -s tests`

Réalisé avec l'aide de Claude (Claude Code) ; j'ai défini les cas limites à traiter et validé les choix ci-dessous.

## Ordre de calcul

1. Règle 1 : remise au volume sur le prix unitaire, seuil évalué sur la quantité totale par `id`.
2. Règle 2 : pack 3 pour 2 sur les prix unitaires déjà remisés.
3. Arrondi half-up à 2 décimales, une seule fois à la fin (`Decimal` en interne).

## Décisions

| Point | Décision |
|---|---|
| Groupes de 3 | Articles de la catégorie triés par prix décroissant, le 3e de chaque groupe est offert. Indépendant de l'ordre du panier, le plus favorable au client. |
| « Même article » | Lignes agrégées par `id` pour trouver le seuil. |
| Seuils | Seul le plus haut seuil atteint s'applique (10 articles : -20 %, pas -30 %). |
| Validation des entrées | Seuls `qty` et `price` négatifs lèvent `ValueError`. Le reste est supposé bien formé (clés absentes de `rules` tolérées, `rules=None` non). |

## Performance

O(n log n), sans éclater `qty` en unités : le nombre d'articles offerts dans un bloc est le nombre de multiples de 3 entre `position` et `position + qty`, soit `(position + qty) // 3 - position // 3`.
