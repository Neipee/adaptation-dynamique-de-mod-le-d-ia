from google import genai
from config import API_KEY
  
client = genai.Client(api_key=API_KEY)

print("--- LISTE DES MODÈLES DISPONIBLES ---")
for m in client.models.list():
    if "generateContent" in m.supported_actions:
        print(f"{m.name}")