# notes_manager.py

import json
import os
import logging
from datetime import datetime
import uuid


class Note:
    def __init__(self, title, content, tags=None, created_at=None, note_id=None):
        self.id = note_id if note_id is not None else str(uuid.uuid4())
        self.title = title
        self.content = content
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "tags": self.tags
        }

class NotesManager:
    def __init__(self, filename='data/notes.json'):
        self.filename = filename
        self.notes = []
        self._load_notes()

    def _load_notes(self):
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
        try:
            with open(self.filename, 'w') as file:
                json.dump([note.to_dict() for note in self.notes], file, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde des notes : {e}")

    def add_note(self, note):
        self.notes.append(note)
        self._save_notes()
        logging.info(f"Note ajoutée : {note.title}")

    def update_note(self, note_id, title, content, tags):
        try:
            for note in self.notes:
                if note.id == note_id:
                    note.title = title
                    note.content = content
                    note.tags = tags
                    note.created_at = datetime.now().isoformat()
                    self._save_notes()
                    logging.info(f"Note mise à jour : {note.title}")
                    return
            raise ValueError("Note not found")
        except ValueError as e:
            logging.error(f"Erreur lors de la mise à jour de la note : {e}")
            raise

    def delete_note(self, note_id):
        try:
            self.notes = [note for note in self.notes if note.id != note_id]
            self._save_notes()
            logging.info(f"Note supprimée avec l'id : {note_id}")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la note : {e}")

    def search_notes(self, query):
        try:
            return [note for note in self.notes if query.lower() in note.title.lower() or any(query.lower() in tag.lower() for tag in note.tags)]
        except Exception as e:
            logging.error(f"Erreur lors de la recherche de notes : {e}")
            return []

    def get_notes(self):
        return self.notes
