from gemini_ask import demander_a_gemini
from prompt_analyse import analyse

MODELS = [
    "models/gemma-3-4b-it",
    "models/gemini-flash-latest",
    "models/gemini-3.1-flash-lite-preview",
    "models/gemini-2.5-pro",
    "models/deep-research-pro-preview-12-2025"
]


def model_from_taux(taux):
    taux = max(0, min(100, taux))

    index = int(taux / 20)

    if index == 5:
        index = 4

    return index


def select_model(prompt):
    
    taux = analyse(prompt)

    start_index = model_from_taux(taux)

    for i in range(start_index, len(MODELS)):

        model = MODELS[i]

        print("Essai avec :", model)

        try:

            response = demander_a_gemini(prompt, model)

            text = str(response)

            if "error" in text.lower():
                print("Erreur détectée dans la réponse -> modèle suivant")
                continue

            if hasattr(response, "text"):
                return response.text.strip()

            return text.strip()

        except Exception as e:

            err = str(e).lower()

            if "error" in err:
                print("Erreur API détectée -> modèle suivant")
                continue

            raise e

    return "Erreur : aucun modèle disponible."