
from Deck import Deck
from Joueur import Joueur
from Pli import Pli

class Partie:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.deck = Deck()
        self.manche = 1
        self.joueur_debut_pli_suivant = None
        self.dernier_gagnant = None
        self.index_debut_manche = 0
        self.mode_score = self.choisir_mode_score()
        self.joueur_debut_pli_suivant = None 

    def choisir_mode_score(self):
        print("Choisissez le mode de score :")
        print("1 - Classique (mise exacte = points, sinon pénalité)")
        print("2 - Rascal (points fixes selon précision)")
        print("3 - Rascal + Boulet de canon (plus risqué)")
        choix = input("Entrez 1, 2 ou 3 : ")
        if choix == "2":
            return "rascal"
        elif choix == "3":
            return "boulet"
        else:
            return "classique"

    def lancer(self):
        total_cartes = len(self.deck.cartes)
        nb_joueurs = len(self.joueurs)
        max_manches = total_cartes // nb_joueurs

        print(f"Nombre de joueurs : {nb_joueurs}")
        print(f"Nombre maximum de manches autorisées : {max_manches}")

        for manche in range(1, max_manches + 1):
            print(f"\\n--- Manche {manche} ---")
            self.jouer_manche(manche)

    def jouer_manche(self, nb_cartes):
        self.index_debut_manche = (self.index_debut_manche + 1) % len(self.joueurs)
        self.deck = Deck() #à modifier, deck recréé à chaque fois on dirait, à voir si modif nécessaire
        self.deck.melanger()

        for joueur in self.joueurs:
            joueur.main = [self.deck.tirer() for _ in range(nb_cartes)]
            joueur.plis = []
            print(f"{joueur.nom} reçoit {len(joueur.main)} cartes.")

        paris = self.phase_de_mise(nb_cartes)

        for pli in range(nb_cartes):
            self.jouer_pli(pli)

        self.comptabiliser_points(paris, nb_cartes)

    def phase_de_mise(self, nb_cartes):
        paris = {}
        for joueur in self.joueurs:
            mise = int(input(f"{joueur.nom}, combien de plis pensez-vous gagner ? "))
            choix_rascal = None
            if self.mode_score == "boulet":
                choix_rascal = input("Boulet de canon ? (o/n) ").lower() == 'o'
            paris[joueur] = {"mise": mise, "boulet": choix_rascal}
        return paris

def jouer_pli(self, numero_pli):
    print(f"\nPli {numero_pli + 1}")
    cartes_jouees = []
    couleur_demandee = None

    for i, joueur in enumerate(self.joueurs):
        print(f"\n{joueur.nom} joue...")
        self.afficher_infos_main(joueur)

        # Détermination de la couleur demandée à partir de la première carte
        if i == 0:
            cartes_valides = list(range(len(joueur.main)))
        else:
            _, premiere_carte = cartes_jouees[0]
            if hasattr(premiere_carte, "color"):
                couleur_demandee = premiere_carte.color
                print(f"Couleur demandée : {couleur_demandee}")
            else:
                couleur_demandee = None

            # Appel à la logique centralisée
            cartes_valides = Pli.cartes_autorisees(joueur.main, couleur_demandee)

        # Affichage de la main avec statut jouable ou non
        print("Votre main :")
        for idx, carte in enumerate(joueur.main):
            info = f" ({carte.info()})" if hasattr(carte, "info") else ""
            prefix = "🔓" if idx in cartes_valides else "🔒"
            status = "" if idx in cartes_valides else " (bloquée)"
            print(f"{prefix} {idx}: {carte}{info}{status}")

        # Choix du joueur (doit être valide)
        while True:
            try:
                choix = int(input("Choisissez une carte à jouer (index autorisé uniquement) : "))
                if choix not in cartes_valides:
                    print("Cette carte est bloquée. Choisissez une autre.")
                    continue
                carte = joueur.main.pop(choix)
                break
            except (ValueError, IndexError):
                print("Choix invalide. Réessayez.")

        print(f"{joueur.nom} joue {carte}")

        # Activation de l'effet si disponible
        if hasattr(carte, "effet") and hasattr(carte.effet, "activer"):
            print(f"{joueur.nom} active l'effet de {carte.nom} !")
            carte.effet.activer(self, joueur, carte)

        cartes_jouees.append((joueur, carte))

    # Résolution du pli
    pli = Pli(cartes_jouees)
    gagnant = pli.gagnant()

    if gagnant:
        print(f"\n{gagnant.nom} remporte le pli")
        gagnant.plis.append(pli)
    else:
        print("\nPersonne ne remporte le pli (Kraken a été joué)")

    # Calcul des points bonus
    bonus = pli.points_bonus()
    for joueur, points in bonus.items():
        if points > 0:
            print(f"💰 Bonus : {joueur.nom} gagne +{points} points bonus pour ce pli.")
            joueur.points += points



def afficher_infos_main(self, joueur):
    print(f"\nEffets des cartes spéciales de {joueur.nom} :")

    for carte in joueur.main:
        couleur = "\033[0m"  # reset par défaut

        if hasattr(carte, "color"):
            if carte.color == "jaune":
                couleur = "\033[93m"  # jaune vif
            elif carte.color == "vert":
                couleur = "\033[92m"  # vert clair
            elif carte.color == "mauve":
                couleur = "\033[95m"  # magenta (violet rose)
            elif carte.color == "noir":
                couleur = "\033[90m"  # gris foncé (atout)

        else:
            if "Tigresse" in carte.nom or "Pirate" in carte.nom:
                couleur = "\033[91m"  # rouge vif
            elif "Sirène" in carte.nom:
                couleur = "\033[94m"  # bleu
            elif carte.nom == "Fuite":
                couleur = "\033[97m"  # blanc éclatant
            elif carte.nom == "Skull King":
                couleur = "\033[33m"  # jaune foncé ~ marron
            elif carte.nom == "Kraken":
                couleur = "\033[35m"  # magenta foncé
            elif carte.nom == "Baleine blanche":
                couleur = "\033[96m"  # cyan très clair

        info = carte.info() if hasattr(carte, "info") else "Pas d'effet"
        print(f"{couleur}- {carte.nom} : {info}\033[0m")


def afficher_infos_main(self, joueur):
    print(f"\nEffets des cartes spéciales de {joueur.nom} :")
    for carte in joueur.main:
        if hasattr(carte, 'info'):
            print(f" - {carte.name} : {carte.info()}")

def resoudre_pli(self, plis):
    special_order = [("Kraken", 5), ("Baleine blanche", 4), ("Skull King", 3), ("Pirate", 2), ("Sirène", 1)]
    names = [c.name for _, c in plis]

    if "Kraken" in names and "Baleine blanche" in names:
        idx_k = names.index("Kraken")
        idx_b = names.index("Baleine blanche")
        if idx_k > idx_b:
            return None  # Kraken dévore tout
        else:
            return self.evaleurr_baleine(plis)

    if "Kraken" in names:
        return None

    if "Baleine blanche" in names:
        return self.evaleurr_baleine(plis)

    # Sinon : priorité Skull King > Pirate > Sirène > Atout > Couleur
    # Simplification à améliorer
    return plis[0][0]  # Par défaut : premier joueur

def evaleurr_baleine(self, plis):
    numeriques = [(j, c) for j, c in plis if hasattr(c, 'valeur')]
    if not numeriques:
        return None
    return max(numeriques, key=lambda jc: jc[1].valeur)[0]

def comptabiliser_points(self, paris, nb_cartes):
    print("\n--- Résultats de la manche ---")

    # 1. Calcul des points classiques
    for joueur in self.joueurs:
        mise = paris[joueur]["mise"]
        plis_gagnes = len(joueur.plis)
        ecart = abs(mise - plis_gagnes)

        if self.mode_score == "classique":
            if mise == plis_gagnes:
                points = 20 * mise if mise > 0 else 10 * nb_cartes
            else:
                points = -10 * ecart if mise > 0 else -10 * nb_cartes

        elif self.mode_score == "rascal":
            if ecart == 0:
                points = 10 * nb_cartes
            elif ecart == 1:
                points = 5 * nb_cartes
            else:
                points = 0

        elif self.mode_score == "boulet":
            if paris[joueur]["boulet"]:
                points = 15 * nb_cartes if ecart == 0 else 0
            else:
                if ecart == 0:
                    points = 10 * nb_cartes
                elif ecart == 1:
                    points = 5 * nb_cartes
                else:
                    points = 0

        joueur.points += points
        print(f"{joueur.nom} : {points:+} pts (mise: {mise}, plis: {plis_gagnes})")

    # 2. Ajout des bonus de cartes (14, sirène, skull king, etc.)
    for joueur in self.joueurs:
        for pli in joueur.plis:
            bonus_dict = pli.points_bonus()
            for j, b in bonus_dict.items():
                if b > 0:
                    print(f"💎 Bonus : {j.nom} gagne +{b} points bonus dans un pli.")
                    j.points += b

    # 3. 🎯 Bonus Butin
    for joueur_bonus in self.joueurs:
        mise_bonus = paris[joueur_bonus]["mise"]
        plis_bonus = len(joueur_bonus.plis)

        if mise_bonus != plis_bonus:
            continue  # pas de bonus si mise ratée

        for pli in joueur_bonus.plis:
            for poseur, carte in pli.cartes_jouees:
                if carte.nom == "Butin" and poseur != joueur_bonus:
                    mise_poseur = paris[poseur]["mise"]
                    plis_poseur = len(poseur.plis)
                    if mise_poseur == plis_poseur:
                        print(f"💰 Bonus Butin : {joueur_bonus.nom} gagne +20 points grâce au Butin posé par {poseur.nom}")
                        joueur_bonus.points += 20
                        break  # un seul bonus par manche suffit

