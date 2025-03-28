from flask import Blueprint, render_template

# This function is called by the ModuleManager.py file
# It is responsible for setting up the routes for the module
def init_routes(blueprint: Blueprint):

    @blueprint.route('/')
    def example():
        return render_template('example.html')

    return example
