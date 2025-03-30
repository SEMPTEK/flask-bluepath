from flask import Flask, Blueprint
import os
import importlib


def register_module(module_name: str, modules_directory: str):
    '''Initialize a module using importlib and Flask blueprints.'''
    root_path = os.path.join(modules_directory, module_name)
    static_url_path = os.path.join(module_name, "static")
    static_fp = os.path.join(modules_directory, module_name, "static")
    template_fp = os.path.join(modules_directory, module_name, "templates")
    bp = Blueprint(module_name, module_name, root_path=root_path, static_url_path=static_url_path, static_folder=static_fp, template_folder=template_fp)
    module_routing_import = f".{module_name}.routing"
    bp_routing = importlib.import_module(module_routing_import, package=modules_directory)
    try:
        bp_routing.init_routes(bp)
    except ImportError as e:
        print(e)
        return False
    return True


class ModuleManager:
    '''
    Module Manager is the core class of the bluepath system. Load this to enable the bluepath auto-import system for modules.
    '''
    required_subdirectories = [
        'templates',
        'static',
        'routing.py',
    ]

    def __init__(self, app: Flask, rel_dir: str = "modules", include: list = [], exclude: list = [], kill_the_beauty: bool = False):
        self.app = app
        self.relative_directory = app.config.get("MODULES_DIRECTORY") or rel_dir
        self.abs_path = os.path.join(os.getcwd(), self.relative_directory)
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
        with open("ascii_art.dat", "r") as f:
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
            item_path = os.path.join(self.relative_directory, item)
            excluded = os.path.basename(item_path) in self.excluded_dir_names
            included = os.path.basename(item_path) in self.included_dir_names or len(self.included_dir_names) == 0
            if not excluded and included:
                self.load_module(item, os.path.join(self.relative_directory, item))

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
        self.__check_if_directory_matches_module_structure(path)
        print(f"Loading {name} module from {path}")
        register_module(name, self.relative_directory)

if __name__ == "__main__":
    APP = Flask(__name__)
    ModuleManager(APP)
