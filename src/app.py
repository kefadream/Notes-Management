# app.py
import tkinter as tk
from tkinter import ttk
from config import load_config
from src.managers import *
from src.frames import NoteListFrame, NotePreviewFrame
from src.notes_manager_helper import NotesManagerHelper
from src.utils import ImageButton, toggle_fullscreen, toggle_theme
class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Notes")
        self.config = load_config()
        print(f"Configuration chargée : {self.config}")  # Ajoutez cette ligne pour vérifier la configuration chargée
        if 'icons' not in self.config:
            raise KeyError("La configuration ne contient pas la section 'icons'")
        self.manager = NotesManager()
        self.theme_manager = ThemeManager()
        self.theme_manager.set_theme(self.config.get('theme', 'light'))

        self.helper = NotesManagerHelper(self)

        self.create_action_frame()  # Crée le frame pour les actions

        main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_paned.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        left_frame = ttk.Frame(main_paned)
        right_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=3)

        self.create_notes_tree(left_frame)
        self.create_note_preview_frame(right_frame)

        self.theme_manager.apply_theme(root)

        self.fullscreen = True
        root.attributes('-fullscreen', self.fullscreen)

        self.create_toggle_fullscreen_button()

    def create_toggle_fullscreen_button(self):
        button_frame = ttk.Frame(self.root)
        button_frame.place(anchor="ne", relx=1.0, rely=0.0, x=-10, y=10)

        toggle_fullscreen_button = ttk.Button(button_frame, text="⤢", command=self.toggle_fullscreen)
        toggle_fullscreen_button.pack()

        self.theme_label = ttk.Label(button_frame, text=f"Thème: {self.theme_manager.theme}")
        self.theme_label.pack(side=tk.BOTTOM)

    def toggle_fullscreen(self):
        self.fullscreen = toggle_fullscreen(self.root, self.fullscreen)

    def create_action_frame(self):
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

        create_group = ttk.LabelFrame(action_frame, text="Gestion des Notes", padding="10")
        create_group.pack(side=tk.LEFT, padx=5, pady=5)

        create_button = ImageButton(create_group, self.config['icons']['create'], command=self.helper.open_create_dialog, size=(32, 32))
        create_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(create_group, text="Créer").pack(side=tk.LEFT, padx=5)

        delete_button = ImageButton(create_group, self.config['icons']['delete'], command=self.helper.open_delete_dialog, size=(32, 32))
        delete_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(create_group, text="Supprimer").pack(side=tk.LEFT, padx=5)

        tag_group = ttk.LabelFrame(action_frame, text="Gestion des Tags", padding="10")
        tag_group.pack(side=tk.LEFT, padx=5, pady=5)

        add_tag_button = ImageButton(tag_group, self.config['icons']['add'], command=self.helper.open_add_tag_dialog, size=(32, 32))
        add_tag_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(tag_group, text="Ajouter").pack(side=tk.LEFT, padx=5)

        delete_tag_button = ImageButton(tag_group, self.config['icons']['delete'], command=self.helper.open_delete_tag_dialog, size=(32, 32))
        delete_tag_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(tag_group, text="Supprimer").pack(side=tk.LEFT, padx=5)

        theme_group = ttk.LabelFrame(action_frame, text="Apparence", padding="10")
        theme_group.pack(side=tk.LEFT, padx=5, pady=5)

        theme_button = ttk.Button(theme_group, text="Changer le thème", command=self.toggle_theme)
        theme_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(theme_group, text="Thème").pack(side=tk.LEFT, padx=5)

    def toggle_theme(self):
        toggle_theme(self.theme_manager, self.config, self.root)
        self.theme_label.config(text=f"Thème: {self.theme_manager.theme}")

    def refresh_notes(self):
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        for note in self.manager.get_notes():
            self.notes_tree.insert("", "end", values=(note.id, note.title, note.content, ', '.join(note.tags), note.created_at))

    def create_note_list_frame(self, parent):
        self.note_list_frame = NoteListFrame(parent, self.manager.get_notes(), self.update_note_preview)
        self.note_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_note_preview_frame(self, parent):
        self.note_preview_frame = NotePreviewFrame(parent)
        self.note_preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_note_preview(self, note):
        self.note_preview_frame.update_preview(note)

    def create_notes_tree(self, parent):
        self.notes_tree = ttk.Treeview(parent, columns=("id", "title", "content", "tags", "created_at"), show='headings')
        self.notes_tree.heading("id", text="ID")
        self.notes_tree.heading("title", text="Titre")
        self.notes_tree.heading("content", text="Contenu")
        self.notes_tree.heading("tags", text="Tags")
        self.notes_tree.heading("created_at", text="Date de création")
        self.notes_tree.column("id", width=0, stretch=tk.NO)  # Masquer la colonne ID
        self.notes_tree.pack(fill=tk.BOTH, expand=True)
        self.notes_tree.bind("<Double-1>", self.helper.on_tree_double_click)
        self.notes_tree.bind("<<TreeviewSelect>>", self.helper.on_tree_select)
        self.refresh_notes()

def main():
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()