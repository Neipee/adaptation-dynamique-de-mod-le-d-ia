from google import genai
from src.config import API_KEY

def demander_a_gemini(prompt, MODEL_ID="models/gemini-3.1-flash-lite-preview"):
    print(f"Analyse en cours avec {MODEL_ID} ...")
    
    client = genai.Client(api_key=API_KEY)
    try:
        # Envoi du texte
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
    
        resultat = response.text.strip()
        return resultat

    except Exception as e:
        print(f"Erreur : {e}")
        return e
