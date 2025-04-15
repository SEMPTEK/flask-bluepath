from flask import Flask, Blueprint
import os
import importlib


def register_module(module_name: str, modules_dirname: str, app_root_path):
    '''Initialize a module using importlib and Flask blueprints.'''
    path = os.path.join(app_root_path, modules_dirname, module_name)
    bp = Blueprint(module_name, module_name, root_path=f"/{modules_dirname}/{module_name}", static_url_path=f"/{module_name}/static", static_folder=f"{path}/static", template_folder=f"{path}/templates")
    module_routing_import = f".{module_name}.routing"
    bp_routing = importlib.import_module(module_routing_import, package=modules_dirname)
    try:
        bp_routing.init_routes(bp)
    except ImportError as e:
        print(e)
        return None
    return bp


class ModuleManager:
    '''
    Module Manager is the core class of the bluepath system. Load this to enable the bluepath auto-import system for modules.
    '''
    required_subdirectories = [
        'templates',
        'static',
        'routing.py',
    ]

    def __init__(self, app: Flask, rel_path_from_app: str = "Modules", include: list = [], exclude: list = [], kill_the_beauty: bool = False):
        self.app = app
        self.rel_path_to_modules_from_app = f"{rel_path_from_app}"
        self.abs_path_to_modules = os.path.join(app.root_path, rel_path_from_app)
        self.modules_dirname = rel_path_from_app
        self.exclusive_modules = include
        self.excluded_modules = exclude
        if not kill_the_beauty: self.print_graphics()
        if not os.path.exists(self.abs_path_to_modules):
            app.logger.error("Module Directory Not Found.", exc_info=True)
        self.__load_modules_from_directory()

    def print_graphics(self):
        self.print_cool_loading_message()
        self.print_exclusion_list()
        self.print_inclusion_list()

    def print_cool_loading_message(self):
        '''Print an ascii art loading message.'''
        fp = os.path.join(self.app.root_path, "flask_bluepath", "ascii_art.dat")
        with open(fp, "r") as f:
            print(f.read())
            print("\n")

    def print_exclusion_list(self):
        '''Print modules inclusion list to console'''
        print("=" * 5 + " EXCLUDED ITEMS " + "=" * 5)
        print(str(self.excluded_modules))
        print("\n")

    def print_inclusion_list(self):
        '''Print modules exclusion list to console'''
        print("=" * 5 + " INCLUDED ITEMS " + "=" * 5)
        print(str(self.excluded_modules))
        print("\n")

    def __load_modules_from_directory(self):
        '''List all directories in the modules directory and load them as modules if they match the required structure'''
        discovered_dirs = os.listdir(self.abs_path_to_modules)
        for dir in discovered_dirs:
            path = os.path.join(self.abs_path_to_modules, dir)
            if self.__check_if_directory_matches_module_structure(dir):
                self.load_module(dir, path)

    def __check_if_directory_matches_module_structure(self, dirname: str):
        '''Check if a directory contains the required subdirectories'''
        print(f"Checking if directory {dirname} matches module structure")
        dir_path = os.path.join(self.abs_path_to_modules, dirname)
        if not os.path.isdir(dir_path):
            return False
        for subdir in self.required_subdirectories:
            if subdir not in os.listdir(dir_path):
                print(f"    Directory {dirname} does not match module structure: Missing {subdir}\n")
                return False
        print(f"    Directory {dirname} matches module structure\n")
        return True

    def load_module(self, name: str, abs_path: str):
        '''Load a module into the app'''
        if not self.__check_if_directory_matches_module_structure(abs_path): return
        print(f"Loading {name} module from {abs_path}")
        self.app.register_blueprint(register_module(name, self.modules_dirname, self.app.root_path))
