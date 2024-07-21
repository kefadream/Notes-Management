"""
Dialogue pour afficher les détails d'une note.

Ce module contient la classe NoteDetailsDialog pour créer une interface
permettant d'afficher les détails d'une note.
"""

import tkinter as tk
from tkinter import ttk


class NoteDetailsDialog(tk.Toplevel):
    """
    Dialogue pour afficher les détails d'une note.
    """
    def __init__(self, parent, note):
        """
        Initialise le dialogue de détails de note.
        """
        super().__init__(parent)
        self.title("Détails de la note")

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

        ttk.Button(frame, text="Fermer", command=self.destroy).grid(row=3, column=0, padx=5, pady=5, columnspan=2)