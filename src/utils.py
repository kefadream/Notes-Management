from tkinter import ttk
import tkinter as tk
from config import save_config


class ImageButton(ttk.Button):
    def __init__(self, parent, image_path, command=None, size=(32, 32), **kwargs):
        self.image = tk.PhotoImage(file=image_path)
        self.image = self.image.subsample(int(self.image.width() // size[0]), int(self.image.height() // size[1]))
        super().__init__(parent, image=self.image, command=command, **kwargs)



def toggle_fullscreen(root, fullscreen):
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    return fullscreen


def toggle_theme(theme_manager, config, root):
    current_theme = theme_manager.theme
    new_theme = 'dark' if current_theme == 'light' else 'light'
    theme_manager.set_theme(new_theme)
    save_config({**config, 'theme': new_theme})
    theme_manager.apply_theme(root)
