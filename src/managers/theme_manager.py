# theme.py
from tkinter import ttk


class ThemeManager:
    def __init__(self):
        self.theme = 'light'
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'button_bg': '#e0e0e0',
                'button_fg': '#000000',
                'frame_bg': '#f0f0f0',
                'label_bg': '#ffffff',
                'label_fg': '#000000'
            },
            'dark': {
                'bg': '#333333',
                'fg': '#ffffff',
                'button_bg': '#555555',
                'button_fg': '#ffffff',
                'frame_bg': '#444444',
                'label_bg': '#333333',
                'label_fg': '#ffffff'
            }
        }

    def set_theme(self, theme):
        if theme in self.themes:
            self.theme = theme
            style = ttk.Style()
            style.theme_use('default')
            style.configure('TButton', background=self.themes[theme]['button_bg'],
                            foreground=self.themes[theme]['button_fg'])
            style.configure('TLabel', background=self.themes[theme]['label_bg'],
                            foreground=self.themes[theme]['label_fg'])
            style.configure('TFrame', background=self.themes[theme]['frame_bg'])

    def apply_theme(self, widget):
        theme = self.themes[self.theme]
        widget_type = widget.winfo_class()

        if 'T' in widget_type:  # Check if the widget is a ttk widget
            return

        if 'fg' in widget.keys():
            widget.configure(fg=theme['fg'])
        if 'bg' in widget.keys():
            widget.configure(bg=theme['bg'])

        for child in widget.winfo_children():
            self.apply_theme(child)
