from flask_bluepath import ModuleManager
from flask import Flask

if __name__ == "__main__":
    APP = Flask(__name__)
    ModuleManager(APP, "Modules")
    APP.run(debug=True)
