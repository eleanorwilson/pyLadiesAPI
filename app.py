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
@app.route('/getRecipes', methods=['GET'])
def getRecipes():
    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())
    return jsonify(recipeList), 200

# CREATE - POST
# use ingredients, steps, name
@app.route('/makeRecipe', methods=['POST'])
def makeRecipe():
    # validate
    if ('name' not in request.json) or ('steps' not in request.json) \
    or ('ingredients' not in request.json):
        return jsonify({'error': 'Missing fields'}), 422
    # open content
    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())

    recipeList.append(request.json)
    #write to the file
    with open('db-recipes.json', 'w') as recipeFile:
        json.dump(recipeList, recipeFile, indent=4)
    return jsonify({'body': 'Successfully added'}), 201

# UPDATE - PUT
@app.route('/makeRecipe', methods=['PUT'])
def updateRecipe():
    #validation
    if 'name' not in request.json:
        return jsonify({'error': 'Missing fields'}), 422

    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())

    for recipe in recipeList:
        if recipe['name'] == request.json["name"]:
            for k in request.json:
                if (k.lower() in recipe) and (k.lower() != "name"):
                    recipe[k.lower()] = request.json[k]

    with open('db-recipes.json', 'w') as recipeFile:
        json.dump(recipeList, recipeFile, indent=4)
    return jsonify({'body': recipeList}), 201

# DELETE - DELETE
@app.route('/badRecipe', methods=['DELETE'])
def badRecipe():
    name = request.args.get("name")
    found = False
    if (name == "") or (name==None):
        return jsonify({'error': "check name input"}), 422

    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())

    for recipe in recipeList:
        if recipe["name"] == name:
            recipeList.remove(recipe)
            found = True

    with open('db-recipes.json', 'w') as recipeFile:
        json.dump(recipeList, recipeFile, indent=4)
    message = {"body": "Deleted"} if found else {"body": "Cannot find the record"}
    return jsonify(message), 200

#BONUS - ERROR HANDLING
@app.errorhandler(404)
def notFound(error=None):
    return jsonify({"error": "Sorry we don't recognize this endpoint"}), 404

app.run()
