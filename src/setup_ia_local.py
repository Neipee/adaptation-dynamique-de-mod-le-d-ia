import subprocess

print("Installation de Ollama...")

subprocess.run(
    ["powershell", "-ExecutionPolicy", "Bypass",
     "-Command", "irm https://ollama.com/install.ps1 | iex"],
    shell=True
)

print("Téléchargement du modèle...")

subprocess.run(["ollama", "pull", "llama3"])

print("Installation terminée")