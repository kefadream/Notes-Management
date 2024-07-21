# notes_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from config import load_config, save_config
from src.notes_manager import Note, NotesManager
from src.dialogs import *
from src.theme import ThemeManager


class ImageButton(ttk.Button):
    def __init__(self, parent, image_path, command=None, size=(32, 32), **kwargs):
        self.image = tk.PhotoImage(file=image_path)
        self.image = self.image.subsample(int(self.image.width() // size[0]), int(self.image.height() // size[1]))
        super().__init__(parent, image=self.image, command=command, **kwargs)


class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Notes")
        self.config = load_config()
        self.manager = NotesManager()
        self.theme_manager = ThemeManager()
        self.theme_manager.set_theme(self.config.get('theme', 'light'))

        self.create_action_frame()  # Crée le frame pour les actions

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.notes_tree = ttk.Treeview(main_frame, columns=("id", "title", "content", "tags", "created_at"), show='headings')
        self.notes_tree.heading("id", text="ID")
        self.notes_tree.heading("title", text="Titre")
        self.notes_tree.heading("content", text="Contenu")
        self.notes_tree.heading("tags", text="Tags")
        self.notes_tree.heading("created_at", text="Date de création")
        self.notes_tree.column("id", width=0, stretch=tk.NO)  # Masquer la colonne ID
        self.notes_tree.pack(fill=tk.BOTH, expand=True)
        self.notes_tree.bind("<Double-1>", self.on_tree_double_click)
        self.refresh_notes()

        self.theme_manager.apply_theme(root)

    def create_action_frame(self):
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

        create_button = ImageButton(action_frame, "icons/create.png", command=self.open_create_dialog, size=(32, 32))
        create_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(action_frame, text="Créer une note").pack(side=tk.LEFT, padx=5)

        delete_button = ImageButton(action_frame, "icons/delete.png", command=self.open_delete_dialog, size=(32, 32))
        delete_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(action_frame, text="Supprimer une note").pack(side=tk.LEFT, padx=5)

        add_tag_button = ImageButton(action_frame, "icons/add_tag.png", command=self.open_add_tag_dialog, size=(32, 32))
        add_tag_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(action_frame, text="Ajouter un tag").pack(side=tk.LEFT, padx=5)

        delete_tag_button = ImageButton(action_frame, "icons/remove_tag.png", command=self.open_delete_tag_dialog, size=(32, 32))
        delete_tag_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(action_frame, text="Supprimer un tag").pack(side=tk.LEFT, padx=5)

        theme_button = ttk.Button(action_frame, text="Changer le thème", command=self.toggle_theme)
        theme_button.pack(side=tk.LEFT, padx=5)
        ttk.Label(action_frame, text="Changer le thème").pack(side=tk.LEFT, padx=5)

    def toggle_theme(self):
        current_theme = self.theme_manager.theme
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.theme_manager.set_theme(new_theme)
        save_config({**self.config, 'theme': new_theme})
        self.theme_manager.apply_theme(self.root)

    def open_create_dialog(self):
        NoteCreationDialog(self.root, self.create_note, self.config["tags"], self.theme_manager)

    def create_note(self, title, content, tags):
        try:
            note = Note(title, content, tags)
            self.manager.add_note(note)
            self.refresh_notes()
            messagebox.showinfo("Succès", "Note enregistrée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la création de la note.")

    def open_delete_dialog(self):
        NoteDeleteDialog(self.root, self.manager.get_notes(), self.delete_note)

    def delete_note(self, note_id):
        try:
            self.manager.delete_note(note_id)
            self.refresh_notes()
            messagebox.showinfo("Succès", "Note supprimée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la suppression de la note.")

    def refresh_notes(self):
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        for note in self.manager.get_notes():
            self.notes_tree.insert("", "end", values=(note.id, note.title, note.content, ', '.join(note.tags), note.created_at))

    def on_tree_double_click(self, event):
        selection = self.notes_tree.selection()
        if selection:
            item = self.notes_tree.item(selection[0])
            logging.debug(f"Item sélectionné : {item}")
            if not item['values']:
                logging.error("Aucune valeur trouvée dans l'élément sélectionné.")
                messagebox.showerror("Erreur", "Impossible de trouver les détails de la note sélectionnée.")
                return

            note_id = item['values'][0]
            note = next((note for note in self.manager.get_notes() if note.id == note_id), None)

            if note is None:
                logging.error("Aucune note correspondante trouvée.")
                messagebox.showerror("Erreur", "Impossible de trouver les détails de la note sélectionnée.")
                return

            NoteEditDialog(self.root, note, self.edit_note, self.config["tags"], self.theme_manager)

    def edit_note(self, note_id, title, content, tags):
        try:
            self.manager.update_note(note_id, title, content, tags)
            self.refresh_notes()
            messagebox.showinfo("Succès", "Note modifiée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la modification de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la modification de la note.")

    def open_add_tag_dialog(self):
        AddTagDialog(self.root, self.add_tag, self.theme_manager)

    def add_tag(self, tag):
        if tag and tag not in self.config["tags"]:
            self.config["tags"].append(tag)
            save_config(self.config)
            messagebox.showinfo("Succès", f"Tag '{tag}' ajouté avec succès!")
        else:
            messagebox.showwarning("Attention", "Le tag est vide ou existe déjà.")

    def open_delete_tag_dialog(self):
        DeleteTagDialog(self.root, self.config["tags"], self.delete_tag, self.theme_manager)

    def delete_tag(self, tag):
        if tag in self.config["tags"]:
            self.config["tags"].remove(tag)
            for note in self.manager.get_notes():
                if tag in note.tags:
                    note.tags.remove(tag)
            save_config(self.config)
            self.refresh_notes()
            messagebox.showinfo("Succès", f"Tag '{tag}' supprimé avec succès!")
        else:
            messagebox.showwarning("Attention", "Le tag n'existe pas.")

# Exemple d'utilisation des boutons avec images dans l'interface
def main():
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
