from google import genai
from config import API_KEY



def demander_a_gemini(prompt, model_id):
    print(f"Analyse en cours avec {model_id} ...")
    
    client = genai.Client(api_key=API_KEY)
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
    
        resultat = response.text.strip()
        return resultat

    except Exception as e:
        print(f"Erreur : {e}")
        return e
