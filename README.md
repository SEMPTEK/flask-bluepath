# Flask Modules

## Table of Contents
- [About](#about)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Credits](#credits)

## About
Flask Modules is built for the [Flask](https://palletsprojects.com/projects/flask) framework by [Pallets Projects](https://palletsprojects.com/). This package is designed to allow for quick loading of modules by using the name of the module directory as the name of the corresponding Flask blueprint. The Module Manager will review the directory and determine if the criteria have been met for a module, and it will load it as a blueprint.  
This really is a lightweight and simple setup for automating  your blueprint creation. Enjoy!

## Requirements
- Flask
- os
- importlib

## Getting Started
1. Create a 'Modules' directory in the same directory as your main Python script.
    - Using Flask config variables, you can set the modules directory to any directory within the application. See [Setting the Modules Directory](#setting-the-modules-directory) for more information.
2. 

## Setting the Modules Directory
Setting the modules directory can be done using the flask configuration dictionary.
```python
# How you set the configuration
app.config[""]
# How Flask_Modules pulls the data
app.config.get("MODULES_DIRECTORY")
```

## Credits
Written by John D McLaughlin (SLACKSIRE) and distributed under the [MIT License](/License.md), a copy of which can be found in the License.md file located within this package.

