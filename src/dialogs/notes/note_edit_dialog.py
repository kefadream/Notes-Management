import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import ImageButton
from icons import DONE_ICON, CANCEL_ICON

class NoteEditDialog(tk.Toplevel):
    """
    Classe NoteEditDialog
    Cette classe représente un dialogue pour modifier une note existante.
    """
    def __init__(self, parent, note, callback, tags, theme_manager):
        """
        Initialise le dialogue de modification de note.

        :param parent: La fenêtre parent.
        :param note: La note à modifier.
        :param callback: La fonction de rappel à appeler lors de la modification de la note.
        :param tags: Les tags disponibles.
        :param theme_manager: Le gestionnaire de thème.
        """
        super().__init__(parent)
        self.title("Modifier la note")
        self.callback = callback
        self.note = note
        self.tags = tags
        self.theme_manager = theme_manager

        self.resizable(False, False)

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = ttk.Entry(frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.insert(0, note.title)

        ttk.Label(frame, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_text = tk.Text(frame, height=10, width=40)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)
        self.content_text.insert("1.0", note.content)

        ttk.Label(frame, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.tags_combobox = ttk.Combobox(frame, values=self.tags, width=37)
        self.tags_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.tags_combobox.set(','.join(note.tags))

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)

        save_button = ImageButton(button_frame, DONE_ICON, command=self.save_changes, size=(24, 24))
        save_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ImageButton(button_frame, CANCEL_ICON, command=self.destroy, size=(24, 24))
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.theme_manager.apply_theme(self)

        # Assurez-vous que ces méthodes sont appelées après que la fenêtre soit complètement initialisée
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def save_changes(self):
        """
        Sauvegarde les changements et appelle le callback.
        """
        new_title = self.title_entry.get().strip()
        new_content = self.content_text.get("1.0", tk.END).strip()
        new_tags = self.tags_combobox.get().strip().split(',')

        if new_title and new_content:
            self.callback(self.note.id, new_title, new_content, new_tags)
            self.destroy()
        else:
            messagebox.showwarning("Erreur", "Le titre et le contenu sont requis.")
