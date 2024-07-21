import tkinter as tk
from tkinter import ttk

class NoteListFrame(ttk.Frame):
    def __init__(self, parent, notes, on_select_note):
        super().__init__(parent)
        self.notes = notes
        self.on_select_note = on_select_note

        self.note_listbox = tk.Listbox(self, height=15)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.note_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        for note in notes:
            self.note_listbox.insert(tk.END, note.title)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.note_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_listbox.config(yscrollcommand=scrollbar.set)

    def on_note_select(self, event):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            note = self.notes[selected_index[0]]
            self.on_select_note(note)


class NotePreviewFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Prévisualisation de la Note", padding="10")

        self.title_label = ttk.Label(self, text="Titre:", font=('Helvetica', 12, 'bold'))
        self.title_label.pack(anchor=tk.W, pady=5)

        self.date_label = ttk.Label(self, text="Date de création:", font=('Helvetica', 10))
        self.date_label.pack(anchor=tk.W, pady=5)

        self.content_text = tk.Text(self, height=15, wrap=tk.WORD, state=tk.DISABLED, font=('Helvetica', 10))
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.content_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.config(yscrollcommand=scrollbar.set)

    def update_preview(self, note):
        self.title_label.config(text=f"Titre: {note.title}")
        self.date_label.config(text=f"Date de création: {note.created_at}")
        self.content_text.config(state=tk.NORMAL)
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, note.content)
        self.content_text.config(state=tk.DISABLED)