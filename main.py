"""
Lanceur de l'application de gestion de notes.

Ce module lance l'interface utilisateur pour gérer les notes.
"""

from src.notes_ui import NotesApp
import tkinter as tk
import logging


def setup_logging():
    logging.basicConfig(
        filename='notes_app.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info('Application démarrée.')


if __name__ == "__main__":
    setup_logging()
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
