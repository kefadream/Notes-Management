"""
Dialogue pour ajouter un nouveau tag.

Ce module contient la classe AddTagDialog pour créer une interface
permettant d'ajouter un nouveau tag.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class AddTagDialog(tk.Toplevel):
    """
    Dialogue pour ajouter un nouveau tag.
    """
    def __init__(self, parent, callback, theme_manager):
        """
        Initialise le dialogue d'ajout de tag.
        """
        super().__init__(parent)
        self.title("Ajouter un nouveau tag")
        self.callback = callback
        self.theme_manager = theme_manager
        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Nouveau tag").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.tag_entry = ttk.Entry(frame, width=40)
        self.tag_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Ajouter", command=self.add_tag).grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Button(frame, text="Annuler", command=self.destroy).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    def add_tag(self):
        """
        Ajoute le nouveau tag.
        """
        tag = self.tag_entry.get().strip()
        if tag:
            self.callback(tag)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Le tag ne peut pas être vide.")