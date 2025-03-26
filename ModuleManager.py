from flask import Flask, Blueprint
import os
import importlib


class Module:
    required_subdirectories = ["templates", "static", "routing.py"]

    def __init__(self, app: Flask, name: str, path: str, modules_dir_name: str):
        self.app = app
        self.name = name
        self.path = path
        self.modules_dir_name = modules_dir_name
        self.blueprint = Blueprint(self.name, self.name, root_path=f"/{self.modules_dir_name}/{self.name}", static_url_path=f"/{self.name}/static", static_folder=f"{self.path}/static", template_folder=f"{self.path}/templates")
        self.__init_routes()
        self.app.register_blueprint(self.blueprint)

    def __init_routes(self):
        '''Import the routing module from the module and initialize the routes'''
        bp_routing = importlib.import_module(f".{self.name}.routing", package=f"{self.modules_dir_name}")
        bp_routing.init_routes(self.blueprint)
        return True


class ModuleManager:
    default_modules_directory = "modules"

    def __init__(self, app: Flask):
        self.app = app
        self.modules = {}
        self.modules_directory = None
        self.modules_directory_name = None
        self.excluded_dir_names = [
            "__pycache__",
            "README.md",
            ]
        self.print_cool_loading_message()
        if not self.__find_modules_directory():
            app.logger.error("No modules directory found")
            return
        self.load_modules_from_modules_directory()

    def print_cool_loading_message(self):
        loading_message = '''
    \nNow Loading
==================================================================================================================

    ███████╗██╗      █████╗ ███████╗██╗  ██╗    ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗
    ██╔════╝██║     ██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
    █████╗  ██║     ███████║███████╗█████╔╝     ██╔████╔██║██║   ██║██║  ██║██║   ██║██║     █████╗  ███████╗
    ██╔══╝  ██║     ██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║██║   ██║██║  ██║██║   ██║██║     ██╔══╝  ╚════██║
    ██║     ███████╗██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║╚██████╔╝██████╔╝╚██████╔╝███████╗███████╗███████║
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝
                                                            By: John McLaughlin (SLACKSIRE) under the MIT License
==================================================================================================================
        \n'''
        print(loading_message)

    def __find_modules_directory(self) -> bool:
        '''Check if the app has a configured modules directory. If not, use default directory'''
        config_dir = os.path.join(self.app.root_path, self.app.config.get("MODULES_DIRECTORY")) if self.app.config.get("MODULES_DIRECTORY") else ""
        default_dir = os.path.join(self.app.root_path, self.default_modules_directory)
        if self.__set_modules_directory(config_dir):
            self.modules_directory_name = self.app.config.get("MODULES_DIRECTORY")
            return True
        if self.__set_modules_directory(default_dir):
            self.modules_directory_name = self.default_modules_directory
            return True
        self.app.logger.error("No modules directory found")
        print(f"Attempted to find modules directory at '{config_dir}' and '{default_dir}'\nNo modules directory found.")
        return False

    def __set_modules_directory(self, path: str):
        '''Set the modules directory for the app. Recommned allowing the ModuleManager to find the directory using __find_modules_directory()'''
        print(f"Checking for modules directory at '{path}'")
        if os.path.exists(path):
            self.modules_directory = path
            print(f"    Modules directory found at '{path}'\nSetting modules directory.\n")
            return True
        return False

    def load_modules_from_modules_directory(self):
        '''List all directories in the modules directory and load them as modules if they match the required structure'''
        found_items = os.listdir(self.modules_directory)
        for item in found_items:
            item_path = os.path.join(self.modules_directory, item)
            if not self.check_if_directory_is_excluded(item_path) and self.check_if_directory_matches_module_structure(item_path):
                self.load_module(item, os.path.join(self.modules_directory, item))

    def check_if_directory_is_excluded(self, path: str):
        '''Check if a directory is excluded from being loaded as a module'''
        if os.path.basename(path) in self.excluded_dir_names:
            print(f"Directory {path} is excluded from being loaded as a module\n")
            return True
        return False

    def check_if_directory_matches_module_structure(self, path: str):
        '''Check if a directory contains the required subdirectories'''
        print(f"Checking if directory {path} matches module structure")
        if not os.path.isdir(path):
            return False
        for subdir in Module.required_subdirectories:
            if subdir not in os.listdir(path):
                print(f"    Directory {path} does not match module structure: Missing {subdir}\n")
                return False
        print(f"    Directory {path} matches module structure\n")
        return True

    def load_module(self, name: str, path: str):
        '''Load a module into the app'''
        print(f"Loading {name} module from {path}")
        if name in self.modules:
            print(f"    Module {name} already loaded\n")
            return False
        module = Module(self.app, name, path, self.modules_directory_name)
        if not module:
            return False
        self.modules[name] = module
        return True
