import sys
from pathlib import Path

# Ajouter le dossier parent au sys.path
parent_folder = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_folder))

import sys
from pathlib import Path
from src.gemini_ask import demander_a_gemini
import customtkinter as ctk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Mini Chat Gemini")
app.geometry("1200x700")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

# Frame scrollable pour toutes les réponses
chat_frame = ctk.CTkScrollableFrame(app, width=1150, height=600)
chat_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0,20), sticky="nsew")
chat_frame.grid_columnconfigure(0, weight=1)

current_row = 0  # ligne pour empiler les messages

# Champ Entry
entry = ctk.CTkEntry(app, width=200, placeholder_text="Ton texte ici…")
entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
entry.focus()

# Bouton Enter
button = ctk.CTkButton(app, text="Enter")
button.grid(row=0, column=1, padx=20, pady=20)

def entry_send(event=None):
    global current_row
    value = entry.get().strip()
    if not value:
        return

    entry.delete(0, ctk.END)

    # 1️⃣ Message de l'utilisateur à droite
    chat_frame.update_idletasks()
    frame_width = chat_frame.winfo_width()
    wrap_user = int(frame_width * 0.5)  # 50% largeur max pour nos messages

    user_label = ctk.CTkLabel(chat_frame,
                              text=value,
                              fg_color="#1E90FF",  # bleu
                              corner_radius=10,
                              wraplength=wrap_user,
                              pady=5,
                              padx=5,
                              text_color="white")
    user_label.grid(row=current_row, column=0, padx=(frame_width//2, 10), pady=5, sticky="e")  # à droite
    current_row += 1

    # 2️⃣ Appel à Gemini et affichage à gauche
    awnser = demander_a_gemini(value)
    print("Réponse:", awnser)

    wrap_gemini = int(frame_width * 0.5)  # 50% largeur max pour réponse
    gemini_label = ctk.CTkLabel(chat_frame,
                                text=awnser,
                                fg_color="black",
                                corner_radius=10,
                                wraplength=wrap_gemini,
                                pady=5,
                                padx=5,
                                text_color="white")
    gemini_label.grid(row=current_row, column=0, padx=(10, frame_width//2), pady=5, sticky="w")  # à gauche
    current_row += 1

    # Scroll automatique vers le bas
    chat_frame.update_idletasks()
    chat_frame.yview_moveto(1.0)

# Lier bouton et touche Enter
button.configure(command=entry_send)
entry.bind("<Return>", entry_send)

app.mainloop()