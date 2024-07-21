# Structure du Projet

- `main.py` : Lanceur de l'application.
- `config.py` : Gestion de la configuration de l'application.
- `notes_manager.py` : Gestionnaire des opérations CRUD pour les notes.
- `notes_ui.py` : Interface utilisateur de l'application.
- `theme.py` : Gestion des thèmes de l'application.
- `dialogs/` : Contient les dialogues pour les notes et les tags.

- - `notes/`
- - - `note_creation_dialog.py` : Dialogue pour créer une nouvelle note.
- - - `note_delete_dialog.py` : Dialogue pour supprimer une note existante.
- - - `note_details_dialog.py` : Dialogue pour afficher les détails d'une note.
- - - `note_edit_dialog.py` : Dialogue pour modifier une note existante.

- - `tags/` : 
- - - `add_tag_dialog.py` : Dialogue pour ajouter un nouveau tag.
- - - `delete_tag_dialog` : Dialogue pour supprimer un tag existant.

## Détails des Fichiers

### main.py

Lanceur de l'application de gestion de notes.

```python
"""
Lanceur de l'application de gestion de notes.

Ce module lance l'interface utilisateur pour gérer les notes.
"""

from src.notes_ui import NotesApp
import tkinter as tk
import logging
import os

def setup_logging():
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(
        filename=os.path.join(log_directory, 'notes_app.log'),
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info('Application démarrée.')

if __name__ == "__main__":
    setup_logging()
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
```