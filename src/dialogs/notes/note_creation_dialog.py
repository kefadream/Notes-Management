"""
Dialogue pour créer une nouvelle note.

Ce module contient la classe NoteCreationDialog pour créer une interface
permettant de créer une nouvelle note.
"""
import tkinter as tk
from tkinter import ttk, messagebox


class NoteCreationDialog(tk.Toplevel):
    def __init__(self, parent, callback, tags, theme_manager):
        super().__init__(parent)
        self.title("Créer une nouvelle note")
        self.callback = callback
        self.theme_manager = theme_manager

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = ttk.Entry(frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_text = tk.Text(frame, height=10, width=30)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.tags_entry = ttk.Combobox(frame, values=tags)
        self.tags_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Enregistrer", command=self.save_note).grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)
        ttk.Button(frame, text="Annuler", command=self.destroy).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.theme_manager.apply_theme(self)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        tags = [self.tags_entry.get()]

        if title and content:
            self.callback(title, content, tags)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Le titre et le contenu sont requis!")