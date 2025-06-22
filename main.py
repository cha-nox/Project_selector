from json                   import JSONDecodeError, load
from InquirerPy.inquirer    import select
from os                     import listdir, system, path

def loadSettings(settings_file : str = "settings.json") -> dict[str, str|bool] :
    """Loads settings from settings.json file."""

    try :
        with open(settings_file, 'r', encoding = 'utf-8') as file : return load(file)
    except FileNotFoundError    : print(f"Fichier {settings_file} non trouvé.")
    except JSONDecodeError as e : print(f"Erreur de format JSON dans {settings_file}. : {e}")
    except Exception as e       : print(f"Erreur lors du chargement de {settings_file}. : {e}")
    return {}

def loadProjectsList(directory : str) -> list[str] :
    """Returns a list of available projects folders in the given directory."""

    if not directory or not path.isdir(directory) : return []
    try :
        return sorted(
            f"• {name}"
            for name in listdir(directory)
            if path.isdir(path.join(directory, name))
        )
    except Exception as e :
        print(f"Erreur en lisant {directory} : {e}")
        return []

if __name__ == '__main__' :
    settings            : dict[str, str|bool]   = loadSettings()
    projects_directory  : str                   = settings.get('projects_directory', '')
    cancel_option       : str                   = "× Annuler"
    options             : list[str]             = loadProjectsList(projects_directory)

    # Clearing the terminal
    system('cls')

    # Checking if there are projects
    if options == [] :
        print("Aucun projet trouvé.")
        system('pause')
        exit(2012)

    # Displaying the menu
    choice = select(
        message     = "Sélectionnez un projet à ouvrir.",
        choices     = options + [cancel_option],
        pointer     = "→",
        instruction = "Utilisez ↑ ↓ pour naviguer puis pressez Entrée pour ouvrir le projet."
    ).execute()

    # Processing user's choice
    if choice != cancel_option : system(f'code "{projects_directory}/{choice[2:]}"')