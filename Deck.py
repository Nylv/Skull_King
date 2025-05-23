import random
from Carte import *
from Pirate import *

class Deck:
    def __init__(self):
        self.cartes = []
        self.fosse = []

        couleurs = ['jaune', 'vert', 'mauve']
        for couleur in couleurs:
            for i in range(1, 15):
                self.cartes.append(CarteCouleur(couleur, i))
        for i in range(1, 15):
            self.cartes.append(CarteAtout(i))

        self.cartes += [Esquive() for _ in range(5)]
        self.cartes += [
            Tigresse(),
            RosieLaDouce(),
            WillLeBandit(),
            RascalLeFlambeur(),
            JuanitaJade(),
            HarryLeGeant()
        ]

        self.cartes.append(SkullKing())
        self.cartes += [Sirene() for _ in range(2)]
        self.cartes += [Butin() for _ in range(2)]
        self.cartes.append(Baleine())
        self.cartes.append(Kraken())

        random.shuffle(self.cartes)

    def tirer(self):
        return self.cartes.pop() if self.cartes else None

    def defausser(self, carte):
        self.fosse.append(carte)
    
    def melanger(self):
        random.shuffle(self.cartes)
