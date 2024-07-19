"""
Gestionnaire de Notes

Ce module contient les classes Note et NotesManager pour gérer la création,
la mise à jour, la suppression et la recherche de notes.

Classes:
    Note: Représente une note avec un titre, du contenu, des tags et une date de création.
    NotesManager: Gère les opérations CRUD sur les notes et les enregistre dans un fichier JSON.
"""

import json
import os
import logging
from datetime import datetime


class Note:
    """
    Classe représentant une note.

    Attributes:
        title (str): Le titre de la note.
        content (str): Le contenu de la note.
        tags (list): Une liste de tags associés à la note.
        created_at (str): La date et l'heure de création de la note.
        id (int): L'identifiant unique de la note.
    """
    def __init__(self, title, content, tags=None, created_at=None, note_id=None):
        self.id = note_id if note_id is not None else None
        self.title = title
        self.content = content
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.tags = tags if tags else []

    def to_dict(self):
        """
        Convertit la note en dictionnaire.

        Returns:
            dict: Le dictionnaire représentant la note.
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "tags": self.tags
        }

class NotesManager:
    """
    Classe gérant les opérations CRUD sur les notes.

    Attributes:
        filename (str): Le nom du fichier JSON pour stocker les notes.
        notes (list): La liste des notes.
    """
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = []
        self._load_notes()

    def _load_notes(self):
        """
        Charge les notes depuis le fichier JSON.
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    notes_dicts = json.load(file)
                    self.notes = [Note(**note_dict) for note_dict in notes_dicts]
            else:
                self._save_notes()
        except Exception as e:
            logging.error(f"Erreur lors du chargement des notes : {e}")

    def _save_notes(self):
        """
        Enregistre les notes dans le fichier JSON.
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump([note.to_dict() for note in self.notes], file, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde des notes : {e}")

    def add_note(self, note):
        """
        Ajoute une nouvelle note.

        Args:
            note (Note): La note à ajouter.
        """
        note.id = len(self.notes) + 1
        self.notes.append(note)
        self._save_notes()
        logging.info(f"Note ajoutée : {note.title}")

    def update_note(self, note_id, title, content, tags):
        """
        Met à jour une note existante.

        Args:
            note_id (int): L'identifiant de la note à mettre à jour.
            title (str): Le nouveau titre de la note.
            content (str): Le nouveau contenu de la note.
            tags (list): La nouvelle liste de tags de la note.

        Raises:
            ValueError: Si la note n'est pas trouvée.
        """
        try:
            for note in self.notes:
                if note.id == note_id:
                    note.title = title
                    note.content = content
                    note.tags = tags
                    note.created_at = datetime.now().isoformat()  # Update the timestamp
                    self._save_notes()
                    logging.info(f"Note mise à jour : {note.title}")
                    return
            raise ValueError("Note not found")
        except ValueError as e:
            logging.error(f"Erreur lors de la mise à jour de la note : {e}")
            raise

    def delete_note(self, note_id):
        """
        Supprime une note.

        Args:
            note_id (int): L'identifiant de la note à supprimer.
        """
        try:
            self.notes = [note for note in self.notes if note.id != note_id]
            self._save_notes()
            logging.info(f"Note supprimée avec l'id : {note_id}")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la note : {e}")

    def search_notes(self, query):
        """
        Recherche des notes par titre ou tags.

        Args:
            query (str): La chaîne de recherche.

        Returns:
            list: La liste des notes correspondant à la recherche.
        """
        try:
            return [note for note in self.notes if query.lower() in note.title.lower() or any(query.lower() in tag.lower() for tag in note.tags)]
        except Exception as e:
            logging.error(f"Erreur lors de la recherche de notes : {e}")
            return []

    def get_notes(self):
        """
        Retourne toutes les notes.

        Returns:
            list: La liste de toutes les notes.
        """
        return self.notes
