"""
Dialogue pour créer une nouvelle note.

Ce module contient la classe NoteCreationDialog pour créer une interface
permettant de créer une nouvelle note.
"""

import tkinter as tk
from tkinter import ttk, messagebox

class NoteCreationDialog(tk.Toplevel):
    """
    Dialogue pour créer une nouvelle note.

    Attributes:
        note (Note): La note créée.
    """
    def __init__(self, parent, callback, tags):
        """
        Initialise le dialogue de création de note.

        Args:
            parent (Tk): La fenêtre parent.
            callback (callable): La fonction de rappel pour ajouter la note.
            tags (list): La liste des tags disponibles.
        """
        super().__init__(parent)
        self.title("Créer une nouvelle note")
        self.callback = callback

        ttk.Label(self, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = ttk.Entry(self, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_text = tk.Text(self, height=10, width=30)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.tags_entry = ttk.Combobox(self, values=tags)
        self.tags_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self, text="Enregistrer", command=self.save_note).grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self, text="Annuler", command=self.destroy).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    def save_note(self):
        """
        Enregistre la nouvelle note.
        """
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        tags = [self.tags_entry.get()]

        if title and content:
            self.callback(title, content, tags)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Le titre et le contenu sont requis!")
