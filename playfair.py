"""Chiffrement de Playfair : on saisit le texte clair et la clé, le programme affiche le chiffré."""

import unicodedata


def nettoyer(texte):
    """Met en majuscules, supprime accents/espaces/non-lettres, remplace J par I."""
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    texte = "".join(c for c in texte.upper() if "A" <= c <= "Z")
    return texte.replace("J", "I")


def generer_grille(cle):
    """Construit la grille 5x5 à partir de la clé (I et J fusionnés)."""
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # sans J
    vu = []
    for c in nettoyer(cle) + alphabet:
        if c not in vu:
            vu.append(c)
    return [vu[i:i + 5] for i in range(0, 25, 5)]


def positions(grille):
    """Dictionnaire lettre -> (ligne, colonne)."""
    return {grille[l][c]: (l, c) for l in range(5) for c in range(5)}


def preparer_digrammes(texte):
    """Découpe en paires ; insère X entre deux lettres identiques, complète avec X."""
    texte = nettoyer(texte)
    digrammes = []
    i = 0
    while i < len(texte):
        a = texte[i]
        if i + 1 < len(texte):
            b = texte[i + 1]
            if a == b:
                digrammes.append((a, "X"))
                i += 1
            else:
                digrammes.append((a, b))
                i += 2
        else:
            digrammes.append((a, "X"))
            i += 1
    return digrammes


def chiffrer(clair, cle):
    grille = generer_grille(cle)
    pos = positions(grille)
    resultat = []
    for a, b in preparer_digrammes(clair):
        la, ca = pos[a]
        lb, cb = pos[b]
        if la == lb:  # même ligne -> lettre à droite
            resultat.append(grille[la][(ca + 1) % 5] + grille[lb][(cb + 1) % 5])
        elif ca == cb:  # même colonne -> lettre en dessous
            resultat.append(grille[(la + 1) % 5][ca] + grille[(lb + 1) % 5][cb])
        else:  # rectangle -> on échange les colonnes
            resultat.append(grille[la][cb] + grille[lb][ca])
    return "".join(resultat)


def afficher_grille(grille):
    for ligne in grille:
        print(" ".join(ligne))


def est_valide(texte):
    """Playfair ne travaille que sur des lettres (accents tolérés, espaces ignorés).
    Chiffres, ponctuation et symboles sont refusés."""
    sans_accents = unicodedata.normalize("NFD", texte)
    sans_accents = "".join(c for c in sans_accents if unicodedata.category(c) != "Mn")
    sans_espaces = sans_accents.replace(" ", "")
    return len(sans_espaces) > 0 and all("A" <= c.upper() <= "Z" for c in sans_espaces)


def saisir(message):
    """Redemande la saisie tant qu'elle contient autre chose que des lettres."""
    while True:
        valeur = input(message)
        if est_valide(valeur):
            return valeur
        print("Erreur : uniquement des lettres (A-Z) sont autorisées "
              "(pas de chiffres ni de symboles). Réessaie.")


if __name__ == "__main__":
    clair = saisir("Texte clair : ")
    cle = saisir("Clé : ")

    print("\nGrille de Playfair :")
    afficher_grille(generer_grille(cle))
    print("\nDigrammes :", " ".join(a + b for a, b in preparer_digrammes(clair)))
    print("Texte chiffré :", chiffrer(clair, cle))