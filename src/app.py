from pathlib import Path
import threading
from select_model import select_model
import customtkinter as ctk

parent_folder = Path(__file__).resolve().parent.parent

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Chat Gemini")
app.geometry("1200x700")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

chat_frame = ctk.CTkScrollableFrame(app, width=1150, height=600)
chat_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0,20), sticky="nsew")
chat_frame.grid_columnconfigure(0, weight=1)

current_row = 0

entry = ctk.CTkEntry(app, width=200, placeholder_text="Ton texte ici…")
entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
entry.focus()

button = ctk.CTkButton(app, text="Enter")
button.grid(row=0, column=1, padx=20, pady=20)

animating = False


def animate_dots(label, base="Réponse en cours"):
    if not animating:
        return

    current = label.cget("text")

    if current.endswith("..."):
        label.configure(text=base + ".")
    else:
        label.configure(text=current + ".")

    app.after(400, animate_dots, label, base)


def afficher_reponse(label, answer):
    global animating

    animating = False
    label.configure(text=answer)

    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)


def worker(prompt, label):
    answer = select_model(prompt)
    app.after(0, afficher_reponse, label, answer)


def entry_send(event=None):
    global current_row
    global animating

    value = entry.get().strip()
    if not value:
        return

    entry.delete(0, ctk.END)

    chat_frame.update_idletasks()
    frame_width = chat_frame.winfo_width()

    wrap_user = int(frame_width * 0.5)

    user_label = ctk.CTkLabel(
        chat_frame,
        text=value,
        fg_color="#1f6aa5",
        corner_radius=10,
        wraplength=wrap_user,
        pady=5,
        padx=5,
        text_color="white"
    )

    user_label.grid(row=current_row, column=0, padx=(frame_width//2, 10), pady=5, sticky="e")
    current_row += 1

    wrap_gemini = int(frame_width * 0.5)

    waiting_label = ctk.CTkLabel(
        chat_frame,
        text="Réponse en cours.",
        fg_color="black",
        corner_radius=10,
        wraplength=wrap_gemini,
        pady=5,
        padx=5,
        text_color="white"
    )

    waiting_label.grid(row=current_row, column=0, padx=(10, frame_width//2), pady=5, sticky="w")
    current_row += 1

    animating = True
    animate_dots(waiting_label)

    thread = threading.Thread(target=worker, args=(value, waiting_label))
    thread.daemon = True
    thread.start()

    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)


button.configure(command=entry_send)
entry.bind("<Return>", entry_send)

app.mainloop()