class Effet:
    def activer(self, partie, joueur):
        raise NotImplementedError("L'effet doit être défini.")

class EffetTigresse(Effet):
    def activer(self, partie, joueur, carte):
        print("Tigresse : choisissez le mode d'action.")
        print("1 - Pirate (carte puissante)")
        print("2 - Fuite (carte perdante)")
        while True:
            choix = input("Votre choix (1 ou 2) : ")
            if choix == "1":
                carte.nom = "Pirate - Tigresse"
                print("Tigresse sera jouée comme une Pirate.")
                break
            elif choix == "2":
                carte.nom = "Fuite - Tigresse"
                print("Tigresse sera jouée comme une Fuite.")
                break
            else:
                print("Choix invalide.")

class EffetRosieLaDouce(Effet):
    def activer(self, partie, joueur, carte):
        print("Rosie la Douce : choisissez le joueur qui commencera le prochain pli.")
        for i, j in enumerate(partie.joueurs):
            print(f"{i} : {j.nom}")
        while True:
            try:
                choix = int(input("Indice du joueur : "))
                partie.joueur_debut_pli_suivant = partie.joueurs[choix]
                print(f"{partie.joueur_debut_pli_suivant.nom} commencera le prochain pli.")
                break
            except (ValueError, IndexError):
                print("Choix invalide.")

class EffetWillLeBandit(Effet):
    def activer(self, partie, joueur, carte):
        for _ in range(2):
            nouvelle = partie.deck.tirer()
            if nouvelle:
                joueur.main.append(nouvelle)
        print("Défaussez 2 cartes de votre main :")
        for i, c in enumerate(joueur.main):
            print(f"{i}: {c}")
        for _ in range(2):
            while True:
                try:
                    choix = int(input("Choix de carte à défausser : "))
                    joueur.main.pop(choix)
                    break
                except (ValueError, IndexError):
                    print("Choix invalide.")

class EffetRascalLeFlambeur(Effet):
    def activer(self, partie, joueur, carte):
        print("Rascal : choisissez une mise spéciale secrète.")
        print("0 - parier sur 0 points")
        print("10 - parier sur +10 points si réussite")
        print("20 - parier sur +20 points si réussite")
        while True:
            choix = input("Votre mise spéciale (0/10/20) : ")
            if choix in ["0", "10", "20"]:
                joueur.mise_rascal = int(choix)
                print(f"Rascal parie sur {choix} points !")
                break
            else:
                print("Choix invalide.")

class EffetJuanitaJade(Effet):
    def activer(self, partie, joueur, carte):
        print("🔍 Juanita Jade : voici les cartes non distribuées cette manche :")
        for c in partie.deck.cartes:
            print(f"- {c}")

class EffetHarryLeGeant(Effet):
    def activer(self, partie, joueur, carte):
        print("Harry le Géant : vous pouvez modifier votre mise de ±1 ou la laisser.")
        mise_actuelle = partie.paris[joueur]["mise"]
        print(f"Mise actuelle : {mise_actuelle}")
        print("1 - Laisser la mise telle quelle")
        print("2 - Augmenter de +1")
        print("3 - Réduire de -1")
        while True:
            choix = input("Choix : ")
            if choix == "1":
                print("Mise conservée.")
                break
            elif choix == "2":
                partie.paris[joueur]["mise"] += 1
                print(f"Mise augmentée à {partie.paris[joueur]['mise']}")
                break
            elif choix == "3":
                partie.paris[joueur]["mise"] = max(0, partie.paris[joueur]["mise"] - 1)
                print(f"Mise réduite à {partie.paris[joueur]['mise']}")
                break
            else:
                print("Choix invalide.")


