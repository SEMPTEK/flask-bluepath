from flask import Flask, Blueprint
import os
import importlib


def register_module(module_name: str, modules_dirname: str):
    '''Initialize a module using importlib and Flask blueprints.'''
    path = os.path.join(os.getcwd(), modules_dirname, module_name)
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

    def __init__(self, app: Flask, rel_dir: str = os.path.relpath("Modules"), include: list = [], exclude: list = [], kill_the_beauty: bool = False):
        self.app = app
        self.relative_path = app.config.get("MODULES_DIRECTORY") or rel_dir
        self.abs_path = os.path.join(self.app.root_path, self.relative_path)
        self.excluded_dir_names = exclude
        self.included_dir_names = include

        if not kill_the_beauty:
            self.print_cool_loading_message()
            self.print_exclusion_list()
            self.print_inclusion_list()
        if not os.path.exists(self.abs_path):
            app.logger.error("Module Directory Not Found.", exc_info=True)
        self.__load_modules_from_directory()

    def print_cool_loading_message(self):
        '''Print an ascii art loading message.'''
        fp = os.path.join(os.getcwd(), "flask_bluepath/ascii_art.dat")
        with open(fp, "r") as f:
            print(f.read())
            print("\n")

    def print_exclusion_list(self):
        '''Print modules inclusion list to console'''
        print("=" * 5 + " EXCLUDED ITEMS " + "=" * 5)
        print(str(self.excluded_dir_names))
        print("\n")

    def print_inclusion_list(self):
        '''Print modules exclusion list to console'''
        print("=" * 5 + " INCLUDED ITEMS " + "=" * 5)
        print(str(self.included_dir_names))
        print("\n")

    def __load_modules_from_directory(self):
        '''List all directories in the modules directory and load them as modules if they match the required structure'''
        for item in os.listdir(self.abs_path):
            item_path = os.path.join(self.relative_path, item)
            excluded = os.path.basename(item_path) in self.excluded_dir_names
            included = os.path.basename(item_path) in self.included_dir_names or len(self.included_dir_names) == 0
            if not excluded and included:
                self.load_module(item, os.path.join(self.relative_path, item))

    def __check_if_directory_matches_module_structure(self, path: str):
        '''Check if a directory contains the required subdirectories'''
        print(f"Checking if directory {path} matches module structure")
        if not os.path.isdir(path):
            return False
        for subdir in self.required_subdirectories:
            if subdir not in os.listdir(path):
                print(f"    Directory {path} does not match module structure: Missing {subdir}\n")
                return False
        print(f"    Directory {path} matches module structure\n")
        return True

    def load_module(self, name: str, path: str):
        '''Load a module into the app'''
        if not self.__check_if_directory_matches_module_structure(path): return
        print(f"Loading {name} module from {path}")
        self.app.register_blueprint(register_module(name, self.relative_path))
