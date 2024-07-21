import os
import json
import logging


CONFIG_FILE = 'data/config.json'
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


def setup_logging():
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(
        filename=os.path.join(log_directory, 'notes_app.log'),
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )
    logging.info('Application démarrée.')

def load_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = DEFAULT_CONFIG
        save_config(config)
    except Exception as e:
        logging.error(f"Erreur lors du chargement de la configuration : {e}")
        config = DEFAULT_CONFIG
    logging.info(f"Configuration chargée : {config}")
    return config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde de la configuration : {e}")
        raise
