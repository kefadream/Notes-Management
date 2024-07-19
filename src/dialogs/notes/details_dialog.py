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

    Attributes:
        note (Note): La note à afficher.
    """
    def __init__(self, parent, note):
        """
        Initialise le dialogue de détails de note.

        Args:
            parent (Tk): La fenêtre parent.
            note (Note): La note à afficher.
        """
        super().__init__(parent)
        self.title("Détails de la note")

        ttk.Label(self, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text=note.title).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        content_text = tk.Text(self, height=10, width=30)
        content_text.grid(row=1, column=1, padx=5, pady=5)
        content_text.insert("1.0", note.content)
        content_text.config(state=tk.DISABLED)

        ttk.Label(self, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(self, text=', '.join(note.tags)).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Button(self, text="Fermer", command=self.destroy).grid(row=3, column=0, padx=5, pady=5, columnspan=2)
