# note_creation_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import ImageButton
from icons import DONE_ICON, CANCEL_ICON

class NoteCreationDialog(tk.Toplevel):
    def __init__(self, parent, callback, tags, theme_manager):
        super().__init__(parent)
        self.title("Créer une nouvelle note")
        self.callback = callback
        self.tags = tags
        self.theme_manager = theme_manager

        self.resizable(False, False)

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        ttk.Label(frame, text="Titre").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry = ttk.Entry(frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Contenu").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_text = tk.Text(frame, height=10, width=40)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Tags").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.tags_combobox = ttk.Combobox(frame, values=self.tags, width=37)
        self.tags_combobox.grid(row=2, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)

        save_button = ImageButton(button_frame, DONE_ICON, command=self.save_note, size=(24, 24))
        save_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ImageButton(button_frame, CANCEL_ICON, command=self.destroy, size=(24, 24))
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.theme_manager.apply_theme(self)

        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        tags = self.tags_combobox.get().strip().split(',')

        if title and content:
            try:
                self.callback(title, content, tags)
                self.destroy()
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
        else:
            messagebox.showwarning("Erreur", "Le titre et le contenu sont requis.")
