import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import ImageButton
from icons import DONE_ICON, CANCEL_ICON


class DeleteTagDialog(tk.Toplevel):
    """
    Dialogue pour supprimer un tag existant.

    Ce module contient la classe DeleteTagDialog pour créer une interface
    permettant de supprimer un tag existant.
    """
    def __init__(self, parent, tags, callback, theme_manager, config):
        super().__init__(parent)
        self.title("Supprimer un tag")
        self.callback = callback
        self.theme_manager = theme_manager
        self.config = config

        self.transient(parent)  # Assure que le dialogue est au-dessus de la fenêtre parent
        self.grab_set()  # Capture tous les événements de l'application

        self.resizable(False, False)

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Sélectionner un tag à supprimer :").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.tags_listbox = tk.Listbox(frame)
        self.tags_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        for tag in tags:
            self.tags_listbox.insert(tk.END, tag)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        delete_button = ImageButton(button_frame, DONE_ICON, command=self.delete_tag, size=(24, 24))
        delete_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ImageButton(button_frame, CANCEL_ICON, command=self.destroy, size=(24, 24))
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.theme_manager.apply_theme(self)
        self.focus_set()  # Donne le focus au dialogue
        self.wait_window(self)  # Attend que cette fenêtre soit fermée avant de continuer

    def delete_tag(self):
        selection = self.tags_listbox.curselection()
        if selection:
            tag = self.tags_listbox.get(selection[0])
            self.callback(tag)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un tag à supprimer.")
