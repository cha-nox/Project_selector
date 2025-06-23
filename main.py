from fnmatch                import fnmatch
from InquirerPy.inquirer    import select
from json                   import JSONDecodeError, load
from os                     import listdir, system, path
from sys                    import exit as sysExit

def loadSettings(settings_file : str = 'settings.json') -> dict[str, str|bool] :
    """Loads settings from settings.json file."""

    try :
        with open(settings_file, 'r', encoding = 'utf-8') as file : return load(file)
    except FileNotFoundError    : print(f"Fichier {settings_file} non trouvé.")
    except JSONDecodeError as e : print(f"Erreur de format JSON dans {settings_file}. : {e}")
    except Exception as e       : print(f"Erreur lors du chargement de {settings_file}. : {e}")
    return {}

def checkIgnoredDirectory(directory_name : str, ignored_patterns : list[str]) -> bool :
    """Check if a directory should be ignored based on the ignored patterns."""
    
    for pattern in ignored_patterns :
        if fnmatch(directory_name.lower(), pattern.lower()) : return True
    return False

def loadProjectsList(directory : str, ignored_directories : list[str]) -> list[str] :
    """Returns a list of available projects folders in the given directory, excluding ignored ones."""

    if not directory or not path.isdir(directory) : return []
    try :
        return sorted(
            f"• {name}"
            for name in listdir(directory)
            if path.isdir(path.join(directory, name)) and not checkIgnoredDirectory(name, ignored_directories)
        )
    except Exception as e :
        print(f"Erreur en lisant {directory} : {e}")
        return []

if __name__ == '__main__' :
    settings            : dict[str, str|bool]   = loadSettings()
    projects_directory  : str                   = settings.get('projects_directory', '')
    ignored_directories : list[str]             = settings.get('ignored_directories', [])
    cancel_option       : str                   = "× Annuler"
    options             : list[str]             = loadProjectsList(projects_directory, ignored_directories)

    # Clearing the terminal
    system('cls')

    # Checking if there are projects
    if options == [] :
        print("Aucun projet trouvé.")
        system('pause')
        sysExit(2012)

    # Displaying the menu
    choice = select(
        message     = "Sélectionnez un projet à ouvrir.",
        choices     = options + [cancel_option],
        pointer     = "→",
        instruction = "Utilisez ↑ ↓ pour naviguer puis pressez Entrée pour ouvrir le projet."
    ).execute()

    # Processing user's choice
    if choice != cancel_option : system(f'code "{projects_directory}/{choice[2:]}"')
    sysExit(0)