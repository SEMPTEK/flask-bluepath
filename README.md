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
1. Create a 'Modules' directory and copy the example_module from this directory to use as a template.
    - Using Flask config variables, you can set the modules directory to any directory within the application. See [Setting the Modules Directory](#setting-the-modules-directory) for more information.
2. Build your flask module like you would any standard flask app; with the following modifications:
    - All flask 

## Setting the Modules Directory
Setting the modules directory can be done using the flask configuration dictionary.
```python
# How you set the configuration
app.config[""]
# How Flask_Modules pulls the data
app.config.get("MODULES_DIRECTORY")
```

## Module Structure
📦example_module  
 ┣ 📂static  
 ┃ ┣ 📂css  
 ┃ ┃ ┗ 📜example.css  
 ┃ ┣ 📂images  
 ┃ ┗ 📂js  
 ┃ ┃ ┗ 📜example.js  
 ┣ 📂templates  
 ┃ ┗ 📜example.html  
 ┗ 📜routing.py  

 
 ## Calling Static Files from Templatea
 Calling an image from the blueprint (module's) static folder requires using url_for. See below for the syntax, or view the [Official Jinja Documentation](https://jinja.palletsprojects.com/en/stable/).
 ```
 {{ url_for("<module_name>.static") filename="images/example.png" }}
 ```

## Credits
Written by John D McLaughlin (SLACKSIRE) and distributed under the [MIT License](/License.md), a copy of which can be found in the License.md file located within this package.

