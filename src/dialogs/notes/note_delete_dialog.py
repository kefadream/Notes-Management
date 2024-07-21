import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import ImageButton
from icons import DELETE_ICON, CANCEL_ICON


class NoteDeleteDialog(tk.Toplevel):
    def __init__(self, parent, notes, callback, theme_manager):
        super().__init__(parent)
        self.title("Supprimer des notes")
        self.callback = callback
        self.theme_manager = theme_manager

        self.resizable(False, False)
        self.attributes('-topmost', 'true')  # Priorité d'affichage

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Sélectionner des notes à supprimer :").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.notes_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=15)
        self.notes_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        for note in notes:
            self.notes_listbox.insert(tk.END, note.title)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        delete_button = ImageButton(button_frame, DELETE_ICON, command=self.delete_notes, size=(24, 24))
        delete_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ImageButton(button_frame, CANCEL_ICON, command=self.destroy, size=(24, 24))
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.theme_manager.apply_theme(self)

    def delete_notes(self):
        selected_indices = self.notes_listbox.curselection()
        if selected_indices:
            note_ids = [self.notes_listbox.get(i) for i in selected_indices]
            self.callback(note_ids)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner des notes à supprimer.")
