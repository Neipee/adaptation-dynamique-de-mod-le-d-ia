from select_model import select_model
import subprocess


def save_prompt(prompt):
    file = "prompt.txt"
    with open(file, "w") as f:
        f.write(prompt)
    #subprocess.run(["./programme_c"])


prompt = input("Prompt: ")
taux = 0.8

response = select_model(taux, prompt)

print(f"""Gemini a répondu : 
{response}""")

