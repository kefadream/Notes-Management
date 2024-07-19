"""
Gestion de la configuration pour l'application de gestion de notes.

Ce module contient les fonctions pour charger et sauvegarder la configuration
depuis et vers un fichier config.json.

Fonctions:
    load_config: Charge la configuration depuis le fichier config.json.
    save_config: Enregistre la configuration dans le fichier config.json.
"""

import json
import logging

CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    "tags": ["Travail", "Personnel", "Urgent"],
    "autosave_interval": 10,
    "theme": "clair",
    "default_tags": ["Travail", "Personnel", "Urgent"],
    "backup_path": "backups/",
    "ui_settings": {
        "font_size": 12,
        "font_family": "Arial",
        "bg_color": "#ffffff",
        "fg_color": "#000000"
    }
}

def load_config():
    """
    Charge la configuration depuis le fichier config.json.

    Returns:
        dict: La configuration chargée.
    """
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = DEFAULT_CONFIG
        save_config(config)
    except Exception as e:
        logging.error(f"Erreur lors du chargement de la configuration : {e}")
        config = DEFAULT_CONFIG
    return config

def save_config(config):
    """
    Enregistre la configuration dans le fichier config.json.

    Args:
        config (dict): La configuration à enregistrer.
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde de la configuration : {e}")
        raise
