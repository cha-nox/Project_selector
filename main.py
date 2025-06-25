from enum                   import StrEnum
from fnmatch                import fnmatch
from InquirerPy.inquirer    import select
from json                   import JSONDecodeError, load
from os                     import listdir, makedirs, system
from os.path                import isdir, join
from sys                    import exit as sysExit

class OtherChoices(StrEnum) :
    """Choices for the menu."""
    NEW_PROJECT_OPTION  : str = "+ Nouveau"
    CANCEL_OPTION       : str = "× Annuler"

def loadSettings(settings_file : str = 'settings.json') -> dict[str, str|bool] :
    """Loads settings from settings.json file."""

    try :
        with open(settings_file, 'r', encoding = 'utf-8') as file : return load(file)
    except FileNotFoundError    : print(f"Fichier {settings_file} non trouvé.")
    except JSONDecodeError as e : print(f"Erreur de format JSON dans {settings_file}. : {e}")
    except Exception as e       : print(f"Erreur lors du chargement de {settings_file}. : {e}")
    return {}

def loadProjectsList(directory : str, ignored_directories : list[str]) -> list[str] :
    """Returns a list of available projects folders in the given directory, excluding ignored ones."""

    if not directory or not isdir(directory) : return []
    try :
        return sorted(
            f"• {name}"
            for name in listdir(directory)
            if isdir(join(directory, name)) and not checkIgnoredDirectory(name, ignored_directories)
        )
    except Exception as e :
        print(f"Erreur en lisant {directory} : {e}")
        return []

def checkIgnoredDirectory(directory_name : str, ignored_patterns : list[str]) -> bool :
    """Check if a directory should be ignored based on the ignored patterns."""
    
    for pattern in ignored_patterns :
        if fnmatch(directory_name.lower(), pattern.lower()) : return True
    return False

if __name__ == '__main__' :
    project_path        : str                   = ''
    new_project_name    : str                   = ''
    settings            : dict[str, str|bool]   = loadSettings()
    projects_directory  : str                   = settings.get('projects_directory', '')
    ignored_directories : list[str]             = settings.get('ignored_directories', [])
    options             : list[str]             = loadProjectsList(projects_directory, ignored_directories)

    # Clearing the terminal
    system('cls')

    # Checking if there are projects
    if options == [] :
        print("Aucun projet trouvé.")
        system('pause')
        sysExit(2012)

    # Displaying the menu
    choice : select = select(
        message     = "Sélectionnez un projet à ouvrir.",
        choices     = options + [OtherChoices.NEW_PROJECT_OPTION, OtherChoices.CANCEL_OPTION],
        pointer     = "→",
        instruction = "Utilisez ↑ ↓ pour naviguer puis pressez Entrée pour ouvrir le projet."
    ).execute()

    # Processing user's choice
    match choice :
        case OtherChoices.NEW_PROJECT_OPTION :
            while new_project_name == '' :
                new_project_name = input("Nom du projet : ")
                project_path = join(projects_directory, new_project_name)
                if new_project_name == '' :
                    print("Le nom du projet ne peut pas être vide.")
                elif isdir(project_path) :
                    print("Ce nom de projet est déjà utilisé.")
                    new_project_name = ''
                else : break
            makedirs(project_path)
            system(f'code "{project_path}"')
        case OtherChoices.CANCEL_OPTION : pass
        case _ : system(f'code "{join(projects_directory, choice[2:])}"')
    sysExit(0)