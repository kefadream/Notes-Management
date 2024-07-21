# notes_manager.py
import json
import os
import uuid
from datetime import datetime


class Note:
    def __init__(self, title, content, tags, created_at=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.tags = tags
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        existing_note = next((n for n in self.notes if n.title == note.title and n.content == note.content), None)
        if not existing_note:
            self.notes.append(note)
            self.save_notes()
        else:
            raise ValueError("Note already exists.")

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def get_notes(self):
        return self.notes

    def update_note(self, note_id, title, content, tags):
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.content = content
                note.tags = tags
                self.save_notes()
                break

    def save_notes(self):
        with open('data/notes.json', 'w', encoding='utf-8') as f:
            json.dump([note.__dict__ for note in self.notes], f, ensure_ascii=False, indent=4)

    def load_notes(self):
        if os.path.exists('data/notes.json'):
            with open('data/notes.json', 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
                for note_data in notes_data:
                    note = Note(
                        title=note_data['title'],
                        content=note_data['content'],
                        tags=note_data['tags'],
                        created_at=note_data['created_at']
                    )
                    note.id = note_data['id']  # Ensure the original ID is retained
                    self.notes.append(note)
