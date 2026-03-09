# NeuroChat — Adaptation Dynamique de Modèle d'IA

Un assistant conversationnel qui **choisit automatiquement le modèle Gemini le plus adapté** à la complexité de ta question — du modèle léger pour une question simple, au modèle puissant pour une analyse complexe.

---

## Fonctionnement

```
Prompt utilisateur
       │
       ▼
 prompt_analyse.py         ← score de complexité (0–100)
       │
       ▼
 select_model.py           ← choisit le modèle Gemini correspondant
       │
       ▼
 gemini_ask.py             ← appelle l'API Gemini
       │
       ▼
 Réponse affichée dans app.py
```

### Sélection du modèle

| Score  | Modèle sélectionné                     |
| ------ | -------------------------------------- |
| 0–19   | `gemma-3-4b-it` (léger)                |
| 20–39  | `gemini-flash-latest`                  |
| 40–59  | `gemini-3.1-flash-lite-preview`        |
| 60–79  | `gemini-2.5-pro`                       |
| 80–100 | `deep-research-pro-preview` (puissant) |

Si un modèle renvoie une erreur (quota, surcharge…), le suivant est automatiquement essayé.

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-user/neurochat.git
cd neurochat
```

### 2. Installer les dépendances Python

```bash
pip install google-genai customtkinter
```

### 3. Configurer la clé API

Édite `src/config.py` :

```python
API_KEY = "ta_clé_api_gemini_ici"
```

> Tu peux obtenir une clé gratuite sur [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## Lancement

```bash
python src/app.py
```

---

## Structure du projet

```
.
├── assets/
│   └── api-keys.json       # Clés API (ne pas commiter)
├── src/
│   ├── app.py              # Interface graphique (CustomTkinter)
│   ├── config.py           # Clé API Gemini
│   ├── gemini_ask.py       # Appel à l'API Gemini
│   ├── prompt_analyse.py   # Calcul du score de complexité
│   ├── select_model.py     # Logique de sélection du modèle
│   ├── setup_ia_local.py   # Installation d'Ollama (optionnel)
│   └── test.py             # Liste les modèles disponibles
└── README.md
```

---

## Score de complexité

`prompt_analyse.py` évalue chaque prompt sur 4 critères (25 pts chacun) :

- **Longueur** — nombre de mots (max à 200)
- **Syntaxe** — virgules, parenthèses, deux-points par phrase
- **Sémantique** — richesse du vocabulaire (ratio mots uniques)
- **Structure** — présence de listes, exemples, contraintes, étapes

---

## IA locale (Ollama)

Pour utiliser un modèle local à la place de Gemini, lance :

```bash
python src/setup_ia_local.py
```

Cela installe Ollama et télécharge `llama3` automatiquement.

---

## Tester les modèles disponibles

```bash
python src/test.py
```

Affiche tous les modèles Gemini accessibles avec ta clé API.

---

## Dépendances

| Package         | Rôle                |
| --------------- | ------------------- |
| `google-genai`  | API Gemini          |
| `customtkinter` | Interface graphique |

---

## Licence

Voir [LICENSE](LICENSE).
