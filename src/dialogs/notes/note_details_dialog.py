"""
Dialogue pour afficher les détails d'une note.

Ce module contient la classe NoteDetailsDialog pour créer une interface
permettant d'afficher les détails d'une note.
"""

import tkinter as tk
from tkinter import ttk
from src.utils import ImageButton


class NoteDetailsDialog(tk.Toplevel):
    def __init__(self, parent, note, theme_manager):
        super().__init__(parent)
        self.title("Détails de la note")
        self.theme_manager = theme_manager

        self.resizable(False, False)

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(frame, text=note.title).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(frame, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        content_text = tk.Text(frame, height=10, width=30)
        content_text.grid(row=1, column=1, padx=5, pady=5)
        content_text.insert("1.0", note.content)
        content_text.config(state=tk.DISABLED)

        ttk.Label(frame, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(frame, text=', '.join(note.tags)).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)

        close_button = ImageButton(button_frame, "icons/close.png", command=self.destroy, size=(24, 24))
        close_button.pack(side=tk.LEFT, padx=5)

        self.theme_manager.apply_theme(self)