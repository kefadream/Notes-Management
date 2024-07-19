"""
Dialogue pour supprimer un tag existant.

Ce module contient la classe DeleteTagDialog pour créer une interface
permettant de supprimer un tag existant.
"""

import tkinter as tk
from tkinter import ttk, messagebox

class DeleteTagDialog(tk.Toplevel):
    """
    Dialogue pour supprimer un tag existant.
    """
    def __init__(self, parent, tags, callback):
        """
        Initialise le dialogue de suppression de tag.

        Args:
            parent (Tk): La fenêtre parent.
            tags (list): La liste des tags disponibles.
            callback (callable): La fonction de rappel pour supprimer le tag.
        """
        super().__init__(parent)
        self.title("Supprimer un tag")
        self.callback = callback

        ttk.Label(self, text="Sélectionner un tag à supprimer :").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.tags_listbox = tk.Listbox(self)
        self.tags_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        for tag in tags:
            self.tags_listbox.insert(tk.END, tag)

        ttk.Button(self, text="Supprimer", command=self.delete_tag).grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self, text="Annuler", command=self.destroy).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    def delete_tag(self):
        """
        Supprime le tag sélectionné.
        """
        selection = self.tags_listbox.curselection()
        if selection:
            tag = self.tags_listbox.get(selection[0])
            self.callback(tag)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un tag à supprimer.")
