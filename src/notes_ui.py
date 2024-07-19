"""
Interface Utilisateur pour le Gestionnaire de Notes

Ce module contient la classe NotesApp pour créer une interface graphique
permettant de gérer les notes.

Classes:
    NotesApp: Interface graphique pour gérer les notes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from src.notes_manager import Note, NotesManager
from src.dialogs import NoteCreationDialog, NoteEditDialog, NoteDeleteDialog, AddTagDialog, DeleteTagDialog
from src.config import load_config, save_config


class NotesApp:
    """
    Interface graphique pour gérer les notes.

    Attributes:
        root (Tk): La fenêtre principale de l'application.
        manager (NotesManager): Le gestionnaire de notes.
    """
    def __init__(self, root):
        """
        Initialise l'interface utilisateur.

        Args:
            root (Tk): La fenêtre principale de l'application.
        """
        self.root = root
        self.root.title("Gestionnaire de Notes")

        self.config = load_config()
        self.manager = NotesManager()

        self.create_menu()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.notes_tree = ttk.Treeview(main_frame, columns=("title", "content", "tags", "created_at"), show='headings')
        self.notes_tree.heading("title", text="Titre")
        self.notes_tree.heading("content", text="Contenu")
        self.notes_tree.heading("tags", text="Tags")
        self.notes_tree.heading("created_at", text="Date de création")
        self.notes_tree.pack(fill=tk.BOTH, expand=True)

        self.notes_tree.bind("<Double-1>", self.on_tree_double_click)

        self.refresh_notes()

    def create_menu(self):
        """
        Crée le menu principal de l'application.
        """
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        note_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Notes", menu=note_menu)
        note_menu.add_command(label="Créer une note", command=self.open_create_dialog)
        note_menu.add_command(label="Supprimer une note", command=self.open_delete_dialog)
        note_menu.add_command(label="Ajouter un tag", command=self.open_add_tag_dialog)
        note_menu.add_command(label="Supprimer un tag", command=self.open_delete_tag_dialog)

    def open_create_dialog(self):
        """
        Ouvre le dialogue de création de note.
        """
        NoteCreationDialog(self.root, self.create_note, self.config["tags"])

    def create_note(self, title, content, tags):
        """
        Crée une nouvelle note.

        Args:
            title (str): Le titre de la note.
            content (str): Le contenu de la note.
            tags (list): Les tags de la note.
        """
        try:
            note = Note(title, content, tags)
            self.manager.add_note(note)
            self.refresh_notes()
            messagebox.showinfo("Succès", "Note enregistrée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la création de la note.")

    def open_delete_dialog(self):
        """
        Ouvre le dialogue de suppression de note.
        """
        NoteDeleteDialog(self.root, self.manager.get_notes(), self.delete_note)

    def delete_note(self, note_id):
        """
        Supprime une note.

        Args:
            note_id (int): L'identifiant de la note à supprimer.
        """
        try:
            self.manager.delete_note(note_id)
            self.refresh_notes()
            messagebox.showinfo("Succès", "Note supprimée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la suppression de la note.")

    def refresh_notes(self):
        """
        Rafraîchit la liste des notes affichées.
        """
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)

        for note in self.manager.get_notes():
            self.notes_tree.insert("", "end", values=(note.title, note.content, ', '.join(note.tags), note.created_at))

    def on_tree_double_click(self, event):
        """
        Gère le double-clic sur un élément de l'arbre.

        Args:
            event (Event): L'événement de double-clic.
        """
        selection = self.notes_tree.selection()
        if selection:
            item = self.notes_tree.item(selection[0])
            note_id = [note.id for note in self.manager.get_notes() if note.title == item['values'][0] and note.content == item['values'][1]][0]
            note = [note for note in self.manager.get_notes() if note.id == note_id][0]
            NoteEditDialog(self.root, note, self.edit_note, self.config["tags"])

    def edit_note(self, note_id, title, content, tags):
        """
        Édite une note.

        Args:
            note_id (int): L'identifiant de la note à éditer.
            title (str): Le nouveau titre de la note.
            content (str): Le nouveau contenu de la note.
            tags (list): Les nouveaux tags de la note.
        """
        try:
            self.manager.update_note(note_id, title, content, tags)
            self.refresh_notes()
            messagebox.showinfo("Succès", "Note modifiée avec succès!")
        except Exception as e:
            logging.error(f"Erreur lors de la modification de la note : {e}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors de la modification de la note.")

    def open_add_tag_dialog(self):
        """
        Ouvre le dialogue d'ajout de tag.
        """
        AddTagDialog(self.root, self.add_tag)

    def add_tag(self, tag):
        """
        Ajoute un nouveau tag et l'enregistre dans config.json.

        Args:
            tag (str): Le tag à ajouter.
        """
        if tag and tag not in self.config["tags"]:
            self.config["tags"].append(tag)
            save_config(self.config)
            messagebox.showinfo("Succès", f"Tag '{tag}' ajouté avec succès!")
        else:
            messagebox.showwarning("Attention", "Le tag est vide ou existe déjà.")

    def open_delete_tag_dialog(self):
        """
        Ouvre le dialogue de suppression de tag.
        """
        DeleteTagDialog(self.root, self.config["tags"], self.delete_tag)

    def delete_tag(self, tag):
        """
        Supprime un tag de la configuration et des notes existantes.

        Args:
            tag (str): Le tag à supprimer.
        """
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
