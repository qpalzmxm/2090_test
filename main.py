from core.library_system import LibrarySystem
from ui.console_interface import admin_login, main_menu

def main():
    library = LibrarySystem()
    if admin_login(library):
        main_menu(library)

if __name__ == "__main__":
    main()
