from google import genai
from config import API_KEY


def demander_a_gemini(prompt: str, model_id: str) -> str:
    print(f"Analyse en cours avec {model_id} ...")

    client = genai.Client(api_key=API_KEY)
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        # On relève l'exception pour que select_model puisse la gérer
        raise