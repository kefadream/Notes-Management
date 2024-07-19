# Gestionnaire de Notes

Une application de gestion de notes utilisant Tkinter pour l'interface utilisateur.

## Fonctionnalités

- Création, modification et suppression de notes
- Gestion des tags pour les notes
- Sauvegarde des notes et des tags dans des fichiers JSON
- Interface utilisateur personnalisable

## Installation

1. Clonez le dépôt :
    ```sh
    [git clone https://github.com/votre-utilisateur/gestionnaire-de-notes.git](https://github.com/johndoe1117/NotesManagement.git)
    ```
2. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation

1. Lancez l'application :
    ```sh
    python main.py
    ```

## Structure du Projet

- `main.py` : Lanceur de l'application.
- `config.py` : Gestion de la configuration de l'application.
- `notes_manager.py` : Gestionnaire des opérations CRUD pour les notes.
- `notes_ui.py` : Interface utilisateur de l'application.
- `dialogs/` : Contient les dialogues pour les notes et les tags.

## Dépendances

- `tkinter`
- `json`
- `logging`

## Contribution

Les contributions sont les bienvenues. Veuillez créer une pull request ou ouvrir une issue pour discuter des changements.

## Licence

Ce projet est sous licence MIT.
