from gemini_ask import demander_a_gemini

MODEL_ID = {"m1": "models/gemini-flash-latest"}

def select_model(taux, prompt):
    if (taux > 0.5):
        return demander_a_gemini(prompt)
    else:
        return
