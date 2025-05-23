
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
        
        self.afficher_resultats_finaux()


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
                return self._effet_baleine(plis)

        if "Kraken" in names:
            return None

        if "Baleine blanche" in names:
            return self._effet_baleine(plis)

        # Sinon : priorité Skull King > Pirate > Sirène > Atout > Couleur
        # Simplification à améliorer
        return plis[0][0]  # Par défaut : premier joueur

    def comptabiliser_points(self, paris, nb_cartes):
        print("\n--- Résultats de la manche ---")
        resume = {}

        for joueur in self.joueurs:
            mise = paris[joueur]["mise"]
            plis = len(joueur.plis)
            ecart = abs(mise - plis)
            points_mise = 0
            bonus_total = 0
            observations = []

            # 1. Points de mise
            if self.mode_score == "classique":
                if mise == plis:
                    if mise > 0:
                        points_mise = 20 * mise
                    else:
                        points_mise = 10 * nb_cartes
                else:
                    if mise > 0:
                        points_mise = -10 * ecart
                    else:
                        points_mise = -10 * nb_cartes


            elif self.mode_score == "rascal":
                if ecart == 0:
                    points_mise = 10 * nb_cartes
                elif ecart == 1:
                    points_mise = 5 * nb_cartes
                else:
                    points_mise = 0

            elif self.mode_score == "boulet":
                if paris[joueur]["boulet"]:
                    points_mise = 15 * nb_cartes if ecart == 0 else 0
                else:
                    if ecart == 0:
                        points_mise = 10 * nb_cartes
                    elif ecart == 1:
                        points_mise = 5 * nb_cartes
                    else:
                        points_mise = 0

            joueur.points += points_mise

            # 2. Bonus pli (cartes spéciales)
            for pli in joueur.plis:
                bonus_dict = pli.points_bonus()
                bonus_total += bonus_dict.get(joueur, 0)

            # 3. Bonus Butin
            for pli in joueur.plis:
                for poseur, carte in pli.cartes_jouees:
                    if carte.nom == "Butin" and poseur != joueur:
                        mise_poseur = paris[poseur]["mise"]
                        plis_poseur = len(poseur.plis)
                        if mise == plis and mise_poseur == plis_poseur:
                            bonus_total += 20
                        else:
                            observations.append("Butin raté")

            # 4. Bonus/malus Rascal
            if hasattr(joueur, "mise_rascal"):
                if mise == plis:
                    bonus_total += joueur.mise_rascal
                else:
                    bonus_total -= joueur.mise_rascal
                    observations.append("Rascal échoué")

            if bonus_total == 0 and not observations:
                observations.append("Aucun bonus")

            joueur.points += bonus_total

            # Stock résumé
            resume[joueur] = {
                "mise": mise,
                "plis": plis,
                "points_mise": points_mise,
                "bonus_total": bonus_total,
                "observations": observations,
                "points_finaux": joueur.points
            }

        self.afficher_resume_manche(resume)

    
    def afficher_resume_manche(self, resume):
        print("\n📊 Résumé de la manche :")
        for joueur, data in resume.items():
            print(f"🔹 {joueur.nom}")
            print(f"   Plis remportés : {data['plis']} / {data['mise']}")
            print(f"   Points de mise : {data['points_mise']:+}")
            print(f"   Bonus : {data['bonus_total']:+}")
            print(f"   Observations : {', '.join(data['observations']) if data['observations'] else '—'}")
            print(f"   Score total : {data['points_finaux']}")


    def afficher_resultats_finaux(self):
        print("\n🏁 Fin de la partie — Résultats finaux :")
        classement = sorted(self.joueurs, key=lambda j: j.points, reverse=True)
        for i, joueur in enumerate(classement):
            rang = ["🥇", "🥈", "🥉"][i] if i < 3 else "🎖️"
            print(f"{rang} {joueur.nom} : {joueur.points} pts")

