"""
Dialogue pour confirmer la suppression d'une note.

Ce module contient la classe NoteDeleteDialog pour créer une interface
permettant de confirmer la suppression d'une note.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class NoteDeleteDialog(tk.Toplevel):
    """
    Dialogue pour confirmer la suppression d'une note.
    """
    def __init__(self, parent, notes, callback):
        """
        Initialise le dialogue de suppression de note.
        """
        super().__init__(parent)
        self.title("Supprimer une note")
        self.callback = callback

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Sélectionner une note à supprimer :").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.notes_listbox = tk.Listbox(frame)
        self.notes_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        for note in notes:
            self.notes_listbox.insert(tk.END, f"{note.id}. {note.title}")

        ttk.Button(frame, text="Supprimer", command=self.delete_note).grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Button(frame, text="Annuler", command=self.destroy).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    def delete_note(self):
        """
        Supprime la note sélectionnée.
        """
        selection = self.notes_listbox.curselection()
        if selection:
            note_text = self.notes_listbox.get(selection[0])
            note_id = int(note_text.split('.')[0])
            self.callback(note_id)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une note à supprimer.")