from gemini_ask import demander_a_gemini
from prompt_analyse import analyse

MODELS = [
    "models/gemma-3-4b-it",
    "models/gemini-3.1-flash-lite-preview",
    "models/gemini-flash-latest",
    "models/gemini-2.5-pro",
    "models/deep-research-pro-preview-12-2025",
]

ERROR_KEYWORDS = [
    "quota exceeded",
    "resource has been exhausted",
    "rate limit",
    "permission denied",
    "invalid api key",
    "model not found",
    "service unavailable",
    "unavailable",
    "503",
    "429",
]


def model_from_taux(taux: int) -> int:
    taux = max(0, min(100, taux))
    return min(int(taux / 20), len(MODELS) - 1)


def is_api_error(obj) -> bool:
    """Accepte n'importe quel type (str, Exception, ServerError…)."""
    lowered = str(obj).lower()
    return any(kw in lowered for kw in ERROR_KEYWORDS)


def select_model(prompt: str) -> str:
    taux        = analyse(prompt)
    start_index = model_from_taux(taux)

    print(f"[select_model] score={taux} → départ index {start_index} ({MODELS[start_index]})")

    for i in range(start_index, len(MODELS)):
        model = MODELS[i]
        print(f"[select_model] essai avec : {model}")

        try:
            response = demander_a_gemini(prompt, model)

            # demander_a_gemini peut retourner l'exception elle-même en cas d'erreur
            if isinstance(response, Exception) or is_api_error(response):
                print(f"[select_model] réponse invalide → modèle suivant")
                continue

            return str(response)

        except Exception as e:
            if is_api_error(e):
                print(f"[select_model] exception API ({e}) → modèle suivant")
                continue
            raise

    return "Erreur : aucun modèle disponible."