
class Carte:
    def __init__(self, nom):
        self.nom = nom

    def __repr__(self):
        return self.nom

class CarteEffet(Carte):
    def __init__(self, nom, effet):
        super().__init__(nom)
        self.effet = effet

    def info(self):
        return self.effet

class Pirate(CarteEffet):
    def __init__(self, nom, effet=""):
        super().__init__(nom, effet)

    def effet_special(self, *args, **kwargs):
        raise NotImplementedError("Chaque pirate doit définir son effet spécial.")

class CarteAtout(Carte):
    def __init__(self, couleur="noir", valeur=0):
        super().__init__(f"{valeur} {couleur}")
        self.color = couleur
        self.valeur = valeur

class CarteCouleur(Carte):
    def __init__(self, couleur, valeur):
        super().__init__(f"{valeur} {couleur}")
        self.color = couleur
        self.valeur = valeur

class Esquive(CarteEffet):
    def __init__(self):
        super().__init__("Fuite", "Passe son tour sans chance de remporter le pli")

class Sirene(CarteEffet):
    def __init__(self):
        super().__init__("Sirène", "Bat toutes les cartes numérotées et peut battre Skull King.")

class Kraken(CarteEffet):
    def __init__(self):
        super().__init__("Kraken", "Annule le pli. Toutes les cartes sont défaussées.")

class Baleine(CarteEffet):
    def __init__(self):
        super().__init__("Baleine blanche", "Les cartes spéciales sont annulées. La carte numérotée la plus haute l'emporte.")

class Butin(CarteEffet):
    def __init__(self):
        super().__init__("Butin", "Si vous et le gagnant misez juste, chacun reçoit +20 points.")

class SkullKing(CarteEffet):
    def __init__(self):
        super().__init__("Skull King", "Bat toutes les cartes sauf les sirènes.")
