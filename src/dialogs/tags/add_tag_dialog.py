import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import ImageButton
from icons import DONE_ICON, CANCEL_ICON


class AddTagDialog(tk.Toplevel):
    """
    Dialogue pour ajouter un nouveau tag.

    Ce module contient la classe AddTagDialog pour créer une interface
    permettant d'ajouter un nouveau tag.
    """
    def __init__(self, parent, callback, theme_manager, config):
        super().__init__(parent)
        self.title("Ajouter un nouveau tag")
        self.callback = callback
        self.theme_manager = theme_manager
        self.config = config

        self.transient(parent)  # Assure que le dialogue est au-dessus de la fenêtre parent
        self.grab_set()  # Capture tous les événements de l'application

        self.resizable(False, False)

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Nouveau tag").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.tag_entry = ttk.Entry(frame, width=40)
        self.tag_entry.grid(row=0, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        add_button = ImageButton(button_frame, DONE_ICON, command=self.add_tag, size=(24, 24))
        add_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ImageButton(button_frame, CANCEL_ICON, command=self.destroy, size=(24, 24))
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.theme_manager.apply_theme(self)
        self.focus_set()  # Donne le focus au dialogue
        self.wait_window(self)  # Attend que cette fenêtre soit fermée avant de continuer

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag:
            self.callback(tag)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Le tag ne peut pas être vide.")
