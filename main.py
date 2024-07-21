# main.py

"""
Lanceur de l'application de gestion de notes.

Ce module lance l'interface utilisateur pour gérer les notes.
"""

from src.app import NotesApp
import tkinter as tk
from config import setup_logging


if __name__ == "__main__":
    setup_logging()
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
