class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.main = []
        self.points = 0
        self.plis = []
        self.mise_plis = 0

    def __repr__(self):
        return self.nom

    def regarder_cartes(self):
        print(self.main)
    
    def pioche(self, deck):
        self.main.append(deck.tirer)
    
