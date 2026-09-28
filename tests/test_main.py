import unittest

from main import calculate_total

RULES = {"volume_discounts": {5: 0.10, 10: 0.20}, "bundle_categories": ["book"]}


def line(id_="A", category="tech", price=10, qty=1):
    return {"id": id_, "category": category, "price": price, "qty": qty}


class ValidCases(unittest.TestCase):
    def check(self, cart, expected, rules=RULES):
        self.assertEqual(calculate_total(cart, rules), expected)

    def test_enonce(self):
        cart = [line("A", "book", 10.0, 4), line("B", "book", 15.0, 1), line("C", "tech", 100.0, 1)]
        self.check(cart, 145.0)

    def test_panier_vide(self):
        self.check([], 0.0)

    def test_regles_vides(self):
        cart = [line("A", "book", 10.0, 4), line("B", "book", 15.0, 1)]
        self.check(cart, 55.0, {})

    def test_volume_sans_cumul(self):
        self.check([line(qty=10)], 80.0)

    def test_seuil_exact(self):
        self.check([line(qty=5)], 45.0)
        self.check([line(qty=4)], 40.0)

    def test_meme_id_agrege(self):
        self.check([line("X", qty=2), line("X", qty=3)], 45.0)

    def test_pack_groupes_par_prix_decroissant(self):
        self.check([line("H", "book", 20, 3), line("L", "book", 5, 3)], 50.0)

    def test_pack_sur_prix_remise(self):
        # 5 x 10 EUR -> -10 % = 9 EUR ; 1 offert -> 4 x 9
        self.check([line("A", "book", 10, 5)], 36.0)

    def test_pack_tri_apres_remise(self):
        # A remisé à 9 EUR passe derrière B à 9.5 EUR : offerts = 2 x 9 EUR
        self.check([line("A", "book", 10, 5), line("B", "book", 9.5, 1)], 36.5)

    def test_pack_groupe_a_cheval_sur_deux_lignes(self):
        # tri : 10, 10, 5, 5 -> le 3e (5) est offert
        self.check([line("A", "book", 10, 2), line("B", "book", 5, 2)], 25.0)

    def test_categorie_non_eligible(self):
        self.check([line("A", "tech", 10, 3)], 30.0)

    def test_pack_par_categorie(self):
        rules = {"bundle_categories": ["book", "cd"]}
        self.check([line("A", "book", 10, 2), line("B", "cd", 10, 2)], 40.0, rules)

    def test_prix_zero(self):
        self.check([line(price=0, qty=2)], 0.0)

    def test_quantite_enorme(self):
        self.check([line("Z", "book", 1, 10**12)], 533333333333.6)

    def test_valeurs_negatives_refusees(self):
        for bad in (line(qty=-1), line(price=-1)):
            with self.assertRaises(ValueError):
                calculate_total([bad], RULES)

    def test_arrondi_half_up(self):
        # 2.675 est stocké 2.67499... en float : Decimal(str()) évite l'arrondi à 2.67
        self.check([line(price=2.675)], 2.68)


if __name__ == "__main__":
    unittest.main()
