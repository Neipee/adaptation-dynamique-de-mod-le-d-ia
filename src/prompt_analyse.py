"""
prompt_analyse.py — analyse de complexité d'un prompt, 100 % Python.
Remplace l'appel au binaire C (main / main.exe).
"""

import re
import math
from collections import Counter
from pathlib import Path

parent_folder = Path(__file__).resolve().parent


# ── Analyse principale (remplace le binaire C) ────────────────────────────────

def analyse(prompt: str) -> int:
    """
    Calcule un score de complexité de 0 à 100 pour le prompt donné,
    puis l'écrit dans score.txt (compatibilité avec l'ancien comportement).
    Retourne le score sous forme d'entier.

    Critères (chacun sur 25 pts) :
      1. Longueur         — nb de mots (max à 200)
      2. Syntaxe          — virgules, parenthèses, deux-points par phrase
      3. Sémantique       — diversité du vocabulaire (ratio mots uniques/total)
      4. Structure        — présence de listes, exemples, contraintes, étapes
    """
    mots    = re.findall(r"\b\w+\b", prompt.lower())
    phrases = [p for p in re.split(r"[.!?]+", prompt) if p.strip()]

    nb_mots   = len(mots)
    nb_phrases = max(len(phrases), 1)

    # 1. Score longueur
    score_longueur = min(nb_mots / 200, 1.0) * 25

    # 2. Score syntaxe
    virgules     = prompt.count(",")
    parentheses  = prompt.count("(") + prompt.count(")")
    deux_points  = prompt.count(":")
    complexite   = (virgules + parentheses + deux_points) / nb_phrases
    score_syntaxe = min(complexite / 5, 1.0) * 25

    # 3. Score sémantique
    vocab_unique    = len(set(mots))
    diversite_vocab = vocab_unique / max(nb_mots, 1)
    score_semantique = diversite_vocab * 25

    # 4. Score structure
    structures = 0
    if re.search(r"[-*•]", prompt):           structures += 1
    if "exemple"     in prompt.lower():       structures += 1
    if "contrainte"  in prompt.lower():       structures += 1
    if "étape"       in prompt.lower():       structures += 1
    score_structure = (structures / 4) * 25

    score_total = score_longueur + score_syntaxe + score_semantique + score_structure
    taux = int(round(min(score_total, 100)))

    # Écriture dans score.txt pour la compatibilité
    score_path = parent_folder / "score.txt"
    with open(score_path, "w", encoding="utf-8") as f:
        f.write(str(taux))

    print(f"[analyse] score = {taux}")
    return taux


# ── Analyse détaillée (pour debug / affichage) ────────────────────────────────

def analyser_prompt(prompt: str) -> dict:
    """Retourne un dict détaillé avec tous les sous-scores."""
    mots    = re.findall(r"\b\w+\b", prompt.lower())
    phrases = [p for p in re.split(r"[.!?]+", prompt) if p.strip()]

    nb_mots    = len(mots)
    nb_phrases = max(len(phrases), 1)

    score_longueur = min(nb_mots / 200, 1.0) * 25

    virgules    = prompt.count(",")
    parentheses = prompt.count("(") + prompt.count(")")
    deux_points = prompt.count(":")
    complexite  = (virgules + parentheses + deux_points) / nb_phrases
    score_syntaxe = min(complexite / 5, 1.0) * 25

    vocab_unique    = len(set(mots))
    diversite_vocab = vocab_unique / max(nb_mots, 1)
    score_semantique = diversite_vocab * 25

    structures = 0
    if re.search(r"[-*•]", prompt):         structures += 1
    if "exemple"    in prompt.lower():      structures += 1
    if "contrainte" in prompt.lower():      structures += 1
    if "étape"      in prompt.lower():      structures += 1
    score_structure = (structures / 4) * 25

    score_total = score_longueur + score_syntaxe + score_semantique + score_structure

    return {
        "mots":              nb_mots,
        "phrases":           nb_phrases,
        "score_longueur":    round(score_longueur,   2),
        "score_syntaxe":     round(score_syntaxe,    2),
        "score_semantique":  round(score_semantique, 2),
        "score_structure":   round(score_structure,  2),
        "complexite_totale": round(min(score_total, 100), 2),
    }


# ── Test rapide ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    exemples = [
        "salut, ca va ???",
        "Explique-moi les étapes pour entraîner un réseau de neurones. "
        "Donne un exemple concret avec des contraintes de mémoire.",
    ]
    for p in exemples:
        print(f"\nPrompt : {p!r}")
        print("Détail :", analyser_prompt(p))
        print("Score  :", analyse(p))