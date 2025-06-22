from dotenv                 import load_dotenv
from InquirerPy.inquirer    import select
from os                     import getenv, listdir, system, path

def getProjectsList(directory : str) -> list[str] :
    if not directory or not path.isdir(directory) : return []
    try :
        return sorted(
            f'• {name}'
            for name in listdir(directory)
            if path.isdir(path.join(directory, name))
        )
    except Exception as e :
        print(f"Erreur en lisant {directory} : {e}")
        return []

if __name__ == '__main__' :
    load_dotenv()

    projects_directory  : str       = getenv('PROJECTS_DIRECTORY', '')
    cancel_option       : str       = "× Annuler"
    options             : list[str] = getProjectsList(projects_directory)

    # Clearing the terminal
    system('cls')

    # Checking if there are projects
    if options == [] :
        print("Aucun projet trouvé.")
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