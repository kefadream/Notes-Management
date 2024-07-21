# notes_manager_helper.py
from tkinter import messagebox
import logging
from src.managers import Note
from src.dialogs import *
from config import save_config

class NotesManagerHelper:
    def __init__(self, app):
        self.app = app

    def open_create_dialog(self):
        NoteCreationDialog(self.app.root, self.create_note, self.app.config["tags"], self.app.theme_manager)

    def create_note(self, title, content, tags):
        try:
            note = Note(title, content, tags)
            self.app.manager.add_note(note)
            self.app.refresh_notes()
            messagebox.showinfo("Succès", "Note enregistrée avec succès!")
        except ValueError as e:
            logging.error(f"Erreur lors de la création de la note : {e}")
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            logging.error(f"Erreur lors de la création de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la création de la note.")

    def open_delete_dialog(self):
        NoteDeleteDialog(self.app.root, self.app.manager.get_notes(), self.delete_notes, self.app.theme_manager)

    def delete_notes(self, note_titles):
        try:
            for note_title in note_titles:
                note = next(note for note in self.app.manager.get_notes() if note.title == note_title)
                self.app.manager.delete_note(note.id)
            self.app.refresh_notes()
            messagebox.showinfo("Succès", "Notes supprimées avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression des notes : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la suppression des notes.")

    def on_tree_double_click(self, event):
        selection = self.app.notes_tree.selection()
        if selection:
            item = self.app.notes_tree.item(selection[0])
            logging.debug(f"Item sélectionné : {item}")
            if not item['values']:
                logging.error("Aucune valeur trouvée dans l'élément sélectionné.")
                messagebox.showerror("Erreur", "Impossible de trouver les détails de la note sélectionnée.")
                return

            note_id = item['values'][0]
            note = next((note for note in self.app.manager.get_notes() if note.id == note_id), None)

            if note is None:
                logging.error("Aucune note correspondante trouvée.")
                messagebox.showerror("Erreur", "Impossible de trouver les détails de la note sélectionnée.")
                return

            NoteEditDialog(self.app.root, note, self.edit_note, self.app.config["tags"], self.app.theme_manager)

    def on_tree_select(self, event):
        selection = self.app.notes_tree.selection()
        if selection:
            item = self.app.notes_tree.item(selection[0])
            note_id = item['values'][0]
            note = next((note for note in self.app.manager.get_notes() if note.id == note_id), None)
            if note:
                self.app.update_note_preview(note)

    def edit_note(self, note_id, title, content, tags):
        try:
            self.app.manager.update_note(note_id, title, content, tags)
            self.app.refresh_notes()
            messagebox.showinfo("Succès", "Note modifiée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la modification de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la modification de la note.")

    def open_add_tag_dialog(self):
        AddTagDialog(self.app.root, self.add_tag, self.app.theme_manager, self.app.config)

    def add_tag(self, tag):
        if tag and tag not in self.app.config["tags"]:
            self.app.config["tags"].append(tag)
            save_config(self.app.config)
            messagebox.showinfo("Succès", f"Tag '{tag}' ajouté avec succès!")
        else:
            messagebox.showwarning("Attention", "Le tag est vide ou existe déjà.")

    def open_delete_tag_dialog(self):
        DeleteTagDialog(self.app.root, self.app.config["tags"], self.delete_tag, self.app.theme_manager, self.app.config)

    def delete_tag(self, tag):
        if tag in self.app.config["tags"]:
            self.app.config["tags"].remove(tag)
            for note in self.app.manager.get_notes():
                if tag in note.tags:
                    note.tags.remove(tag)
            save_config(self.app.config)
            self.app.refresh_notes()
            messagebox.showinfo("Succès", f"Tag '{tag}' supprimé avec succès!")
        else:
            messagebox.showwarning("Attention", "Le tag n'existe pas.")
