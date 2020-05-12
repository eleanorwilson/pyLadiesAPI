# Flask API about recipes
# JSON for recipes original source: https://github.com/raywenderlich/recipes/blob/master/Recipes.json
import flask
import json
from flask import request, jsonify, abort

# App is a Flask object.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Welcome- HTML example
@app.route('/', methods=['GET'])
def welcome():
    # Example returning python to it
    return "<h1>Welcome to PyLadies!</h1><p>This is a tutorial over how to create a API using Flask.</p>"

# READ - GET

# CREATE - POST

# UPDATE - PUT

# DELETE - DELETE

#BONUS - ERROR HANDLING

app.run()
