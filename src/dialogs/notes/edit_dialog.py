"""
Dialogue pour éditer une note existante.

Ce module contient la classe NoteEditDialog pour créer une interface
permettant d'éditer une note existante.
"""

import tkinter as tk
from tkinter import ttk, messagebox

class NoteEditDialog(tk.Toplevel):
    """
    Dialogue pour éditer une note existante.

    Attributes:
        note (Note): La note éditée.
    """
    def __init__(self, parent, note, callback, tags):
        """
        Initialise le dialogue d'édition de note.

        Args:
            parent (Tk): La fenêtre parent.
            note (Note): La note à éditer.
            callback (callable): La fonction de rappel pour mettre à jour la note.
            tags (list): La liste des tags disponibles.
        """
        super().__init__(parent)
        self.title("Modifier la note")
        self.callback = callback
        self.note = note

        ttk.Label(self, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = ttk.Entry(self, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.insert(0, note.title)

        ttk.Label(self, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_text = tk.Text(self, height=10, width=30)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)
        self.content_text.insert("1.0", note.content)

        ttk.Label(self, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.tags_entry = ttk.Combobox(self, values=tags)
        self.tags_entry.grid(row=2, column=1, padx=5, pady=5)
        self.tags_entry.set(','.join(note.tags))

        ttk.Button(self, text="Enregistrer", command=self.save_changes).grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self, text="Annuler", command=self.destroy).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    def save_changes(self):
        """
        Enregistre les modifications de la note.
        """
        new_title = self.title_entry.get()
        new_content = self.content_text.get("1.0", tk.END).strip()
        new_tags = self.tags_entry.get().split(',')

        if new_title and new_content:
            self.callback(self.note.id, new_title, new_content, new_tags)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Le titre et le contenu sont requis!")
