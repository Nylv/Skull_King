class Pli:
    def __init__(self, cartes_jouees):
        self.cartes_jouees = cartes_jouees

    def gagnant(self):
        noms = [carte.nom for _, carte in self.cartes_jouees]

        # Kraken + Baleine joués → dernier des deux l’emporte
        if "Kraken" in noms and "Baleine blanche" in noms:
            for joueur, carte in reversed(self.cartes_jouees):
                if carte.nom in ["Kraken", "Baleine blanche"]:
                    return joueur

        # Kraken seul → personne ne gagne
        elif "Kraken" in noms:
            return None

        # Baleine seule → carte numérotée la plus haute gagne
        elif "Baleine blanche" in noms:
            return self._effet_baleine()

        # Sinon résolution standard par priorité
        else:
            return self._resoudre_par_priorite()


    def _effet_baleine(self):
        # Ignorer les cartes spéciales
        cartes_valides = [(j, c) for j, c in self.cartes_jouees if hasattr(c, "valeur")]
        if not cartes_valides:
            return None
        return max(cartes_valides, key=lambda jc: jc[1].valeur)[0]

    def _resoudre_par_priorite(self):
        def carte_prio(carte):
            if carte.nom == "Skull King":
                return (5, 0)
            if carte.nom == "Sirène":
                if any(c.nom == "Skull King" for _, c in self.cartes_jouees):
                    return (6, 0)  # Sirène bat Skull King
                if any("Pirate" in c.nom for _, c in self.cartes_jouees):
                    return (1, 0)  # Sirène perd contre Pirate
                return (3, 0)  # Sinon priorité modérée (bat cartes numérotées)

            if "Pirate" in carte.nom:
                return (2, 0)
            if hasattr(carte, "color") and carte.color == "noir":
                return (1, carte.valeur)
            if hasattr(carte, "valeur"):
                return (0, carte.valeur)
            return (-1, 0)

        meilleures_cartes = sorted(self.cartes_jouees, key=lambda jc: carte_prio(jc[1]), reverse=True)
        return meilleures_cartes[0][0]


    @staticmethod

    def cartes_autorisees(main, couleur_demandee):
        """
        Retourne la liste des indices des cartes que le joueur a le droit de jouer.
        """
        if not couleur_demandee:
            return list(range(len(main)))  # aucune contrainte

        cartes_valides = []
        for i, carte in enumerate(main):
            if not hasattr(carte, "color"):  # carte spéciale (pirate, sirène, etc.)
                cartes_valides.append(i)
            elif carte.color == couleur_demandee:
                cartes_valides.append(i)

        # Si aucune carte de la couleur demandée, tout est autorisé
        if not any(hasattr(c, "color") and c.color == couleur_demandee for c in main):
            return list(range(len(main)))

        return cartes_valides

    def points_bonus(self):
        """
        Retourne un dict {joueur: bonus} pour le joueur ayant gagné le pli,
        en respectant l'ordre d'apparition pour Pirates et Sirènes.
        """
        bonus = {}

        gagnant = self.gagnant()
        if not gagnant:
            return bonus  # pas de gagnant = pas de bonus

        noms_cartes = [c.nom for _, c in self.cartes_jouees]

        # Trouver la carte du gagnant
        carte_gagnante = None
        for joueur, carte in self.cartes_jouees:
            if joueur == gagnant:
                carte_gagnante = carte
                break

        if not carte_gagnante:
            return bonus

        # Bonus 14
        if hasattr(carte_gagnante, "valeur") and carte_gagnante.valeur == 14 and hasattr(carte_gagnante, "color"):
            if carte_gagnante.color in ["jaune", "vert", "mauve"]:
                bonus[gagnant] = 10
            elif carte_gagnante.color == "noir":
                bonus[gagnant] = 20

        # Bonus Sirène bat Skull King (si elle est la première Sirène jouée)
        elif carte_gagnante.nom == "Sirène" and "Skull King" in noms_cartes:
            for joueur, carte in self.cartes_jouees:
                if carte.nom == "Sirène":
                    if joueur == gagnant:
                        bonus[gagnant] = 40
                    break  # seule la première Sirène compte

        # Bonus Skull King bat Pirate
        elif carte_gagnante.nom == "Skull King" and any("Pirate" in n for n in noms_cartes):
            bonus[gagnant] = 30

        # Bonus Pirate bat Sirène (si c’est le premier Pirate joué)
        elif "Pirate" in carte_gagnante.nom and "Sirène" in noms_cartes:
            for joueur, carte in self.cartes_jouees:
                if "Pirate" in carte.nom:
                    if joueur == gagnant:
                        bonus[gagnant] = 20
                    break  # seule le premier Pirate compte

        return bonus

