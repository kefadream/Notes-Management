"""
Initialisation du package dialogs.

Ce module importe toutes les classes de dialogue nécessaires pour l'application.
"""

from .notes import NoteCreationDialog, NoteEditDialog, NoteDeleteDialog, NoteDetailsDialog
from .tags import AddTagDialog, DeleteTagDialog

__all__ = [

    'NoteCreationDialog',
    'NoteEditDialog',
    'NoteDeleteDialog',
    'NoteDetailsDialog',
    'AddTagDialog',
    'DeleteTagDialog'

]
