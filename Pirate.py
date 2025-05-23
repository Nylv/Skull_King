
from Carte import Pirate
from Effet import *

class Tigresse(Pirate):
    def __init__(self):
        super().__init__("Tigresse", "Agit comme une Pirate ou une Fuite, au choix du joueur.")
        self.effet = EffetTigresse()

class RosieLaDouce(Pirate):
    def __init__(self):
        super().__init__("Rosie la Douce", "Choisit le joueur qui commence le prochain pli.")
        self.effet = EffetRosieLaDouce()

class WillLeBandit(Pirate):
    def __init__(self):
        super().__init__("Will le Bandit", "Pioche 2 cartes puis défausse 2 cartes.")
        self.effet = EffetWillLeBandit()

class RascalLeFlambeur(Pirate):
    def __init__(self):
        super().__init__("Rascal le Flambeur", "Parie 0, 10 ou 20 points selon sa réussite.")
        self.effet = EffetRascalLeFlambeur()

class JuanitaJade(Pirate):
    def __init__(self):
        super().__init__("Juanita Jade", "Permet de voir les cartes non distribuées.")
        self.effet = EffetJuanitaJade()

class HarryLeGeant(Pirate):
    def __init__(self):
        super().__init__("Harry le Géant", "Peut modifier sa mise de ±1 après l'avoir faite.")
        self.effet = EffetHarryLeGeant()