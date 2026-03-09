from pathlib import Path
import threading
import time
from select_model import select_model
import customtkinter as ctk
from tkinter import font as tkfont

parent_folder = Path(__file__).resolve().parent.parent

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ── Palette ──────────────────────────────────────────────────────────────────
BG_DEEP      = "#0a0c10"
BG_SURFACE   = "#111318"
BG_CARD      = "#181c24"
ACCENT       = "#4f8ef7"
ACCENT_DIM   = "#1e3a6e"
BUBBLE_USER  = "#1a3a6c"
BUBBLE_BOT   = "#1a1f2e"
TEXT_PRIMARY = "#e8ecf4"
TEXT_MUTED   = "#5a6378"
BORDER       = "#232838"
SUCCESS      = "#3dd68c"

# ── App window ────────────────────────────────────────────────────────────────
app = ctk.CTk()
app.title("NeuroChat")
app.geometry("1100x720")
app.configure(fg_color=BG_DEEP)
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

# ── Header bar ────────────────────────────────────────────────────────────────
header = ctk.CTkFrame(app, fg_color=BG_SURFACE, corner_radius=0, height=56,
                      border_width=1, border_color=BORDER)
header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
header.grid_columnconfigure(1, weight=1)
header.grid_propagate(False)

dot_frame = ctk.CTkFrame(header, fg_color="transparent")
dot_frame.grid(row=0, column=0, padx=18, pady=0, sticky="w")
for color in ("#ff5f57", "#febc2e", "#28c840"):
    ctk.CTkLabel(dot_frame, text="●", text_color=color,
                 font=ctk.CTkFont(size=11)).pack(side="left", padx=3)

title_label = ctk.CTkLabel(
    header, text="NeuroChat",
    font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
    text_color=ACCENT
)
title_label.grid(row=0, column=1, sticky="", pady=0)

status_dot = ctk.CTkLabel(header, text="● Online",
                           font=ctk.CTkFont(size=11),
                           text_color=SUCCESS)
status_dot.grid(row=0, column=2, padx=18, sticky="e")

# ── Chat scrollable area ──────────────────────────────────────────────────────
chat_outer = ctk.CTkFrame(app, fg_color=BG_DEEP)
chat_outer.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
chat_outer.grid_columnconfigure(0, weight=1)
chat_outer.grid_rowconfigure(0, weight=1)

chat_frame = ctk.CTkScrollableFrame(
    chat_outer,
    fg_color=BG_DEEP,
    scrollbar_button_color=BORDER,
    scrollbar_button_hover_color=ACCENT_DIM,
    corner_radius=0
)
chat_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
chat_frame.grid_columnconfigure(0, weight=1)

current_row = 0

# ── Input bar ─────────────────────────────────────────────────────────────────
input_bar = ctk.CTkFrame(app, fg_color=BG_SURFACE, corner_radius=0,
                          border_width=1, border_color=BORDER, height=72)
input_bar.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
input_bar.grid_columnconfigure(0, weight=1)
input_bar.grid_propagate(False)

entry = ctk.CTkEntry(
    input_bar,
    placeholder_text="  Écris ton message…",
    font=ctk.CTkFont(family="Courier New", size=13),
    fg_color=BG_CARD,
    border_color=BORDER,
    border_width=1,
    text_color=TEXT_PRIMARY,
    placeholder_text_color=TEXT_MUTED,
    corner_radius=10,
    height=42
)
entry.grid(row=0, column=0, padx=(18, 10), pady=15, sticky="ew")
entry.focus()

send_btn = ctk.CTkButton(
    input_bar,
    text="  Envoyer  ▶",
    font=ctk.CTkFont(family="Courier New", size=12, weight="bold"),
    fg_color=ACCENT,
    hover_color="#2d6fdb",
    text_color="#ffffff",
    corner_radius=10,
    height=42,
    width=120
)
send_btn.grid(row=0, column=1, padx=(0, 18), pady=15)

animating = False


# ── Helpers ───────────────────────────────────────────────────────────────────
def add_timestamp(row, align="e"):
    t = time.strftime("%H:%M")
    pad_left  = (20, 0)  if align == "e" else (60, 0)
    pad_right = (0, 20) if align == "e" else (0, 60)
    ctk.CTkLabel(
        chat_frame, text=t,
        font=ctk.CTkFont(family="Courier New", size=9),
        text_color=TEXT_MUTED,
        fg_color="transparent"
    ).grid(row=row, column=0,
           padx=(pad_left[0], pad_right[0]),
           pady=(0, 10),
           sticky=align)


def make_bubble(parent, text, fg, text_color, wrap):
    return ctk.CTkLabel(
        parent,
        text=text,
        fg_color=fg,
        corner_radius=14,
        wraplength=wrap,
        pady=10,
        padx=14,
        text_color=text_color,
        font=ctk.CTkFont(family="Courier New", size=13),
        justify="left",
        anchor="w"
    )


# ── Dot animation ─────────────────────────────────────────────────────────────
def animate_dots(label, base="En réflexion"):
    if not animating:
        return
    cur = label.cget("text")
    suffix = cur.replace(base, "")
    new_suffix = "." if suffix == "..." else suffix + "."
    label.configure(text=base + new_suffix)
    app.after(420, animate_dots, label, base)


def afficher_reponse(label, answer, ts_row):
    global animating
    animating = False
    label.configure(text=answer)
    add_timestamp(ts_row, align="w")
    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)
    status_dot.configure(text="● Online", text_color=SUCCESS)


def worker(prompt, label, ts_row):
    answer = select_model(prompt)
    app.after(0, afficher_reponse, label, answer, ts_row)


# ── Send logic ────────────────────────────────────────────────────────────────
def entry_send(event=None):
    global current_row, animating

    value = entry.get().strip()
    if not value:
        return

    entry.delete(0, ctk.END)
    chat_frame.update_idletasks()
    frame_width = max(chat_frame.winfo_width(), 600)
    wrap = int(frame_width * 0.55)

    # User bubble
    user_bubble = make_bubble(chat_frame, value, BUBBLE_USER, TEXT_PRIMARY, wrap)
    user_bubble.grid(row=current_row, column=0,
                     padx=(int(frame_width * 0.3), 24), pady=(8, 0), sticky="e")
    current_row += 1
    add_timestamp(current_row, align="e")
    current_row += 1

    # Bot bubble
    bot_bubble = make_bubble(chat_frame, "En réflexion.", BUBBLE_BOT, TEXT_PRIMARY, wrap)
    bot_bubble.grid(row=current_row, column=0,
                    padx=(24, int(frame_width * 0.3)), pady=(8, 0), sticky="w")
    current_row += 1
    ts_row = current_row
    current_row += 1

    status_dot.configure(text="● Thinking…", text_color="#f5a623")
    animating = True
    animate_dots(bot_bubble)

    t = threading.Thread(target=worker, args=(value, bot_bubble, ts_row))
    t.daemon = True
    t.start()

    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)


send_btn.configure(command=entry_send)
entry.bind("<Return>", entry_send)

app.mainloop()