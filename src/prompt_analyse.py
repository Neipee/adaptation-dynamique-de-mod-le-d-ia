import re
import math
from collections import Counter
import subprocess
from pathlib import Path

parent_folder = Path(__file__).resolve().parent

def analyse(prompt):
    prompt_txt = parent_folder / "prompt.txt"

    # Écrire le prompt dans le fichier
    with open(prompt_txt, "w", encoding="utf-8") as f:
        f.write(prompt)

    # Exécutable + argument
    exe_path = parent_folder / "main"
    subprocess.run([str(exe_path), str(prompt_txt)], check=True)

    # Lire le score généré
    taux_txt = parent_folder / "score.txt"
    with open(taux_txt, "r", encoding="utf-8") as f:
        score = f.read().strip()
        taux = int(score)  # ou float(score) si besoin
        print(taux)
        return taux



def analyser_prompt(prompt):
    mots = re.findall(r"\b\w+\b", prompt.lower())
    phrases = re.split(r"[.!?]+", prompt)

    nb_mots = len(mots)
    nb_phrases = len([p for p in phrases if p.strip() != ""])

    score_longueur = min(nb_mots / 200, 1) * 25

    virgules = prompt.count(",")
    parentheses = prompt.count("(") + prompt.count(")")
    deux_points = prompt.count(":")

    complexite_syntaxe = (virgules + parentheses + deux_points) / max(nb_phrases,1)

    score_syntaxe = min(complexite_syntaxe / 5, 1) * 25
    vocab_unique = len(set(mots))

    diversite_vocab = vocab_unique / max(nb_mots,1)

    score_semantique = diversite_vocab * 25

    structures = 0

    if "-" in prompt or "*" in prompt:
        structures += 1
    if "exemple" in prompt.lower():
        structures += 1
    if "contraintes" in prompt.lower():
        structures += 1
    if "étape" in prompt.lower():
        structures += 1

    score_structure = (structures / 4) * 25

    score_total = score_longueur + score_syntaxe + score_semantique + score_structure

    return {
        "mots": nb_mots,
        "phrases": nb_phrases,
        "score_longueur": round(score_longueur,2),
        "score_syntaxe": round(score_syntaxe,2),
        "score_semantique": round(score_semantique,2),
        "score_structure": round(score_structure,2),
        "complexite_totale": round(score_total,2)
    }


if __name__ == "__main__":
    prompt = 'salut, ca va ???'
    analyse(prompt)