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

# CREATE - POST
# To create a recipe you must have fields - name, ingredients,instructions
@app.route('/makeRecipe', methods=['POST'])
def makeReceipe():
    # Validate required fields
    if ('name' not in request.json) or ('steps' not in request.json) \
    or ('ingredients' not in request.json):
        return jsonify({'error': 'Missing fields'}), 422

    # read file and load contents
    with open('db-recipes.json', 'r', encoding='utf-8') as recipeFile:
        recipeList = json.loads(recipeFile.read())

    #append to the list
    recipeList.append(request.json)
    # write to the file
    with open('db-recipes.json','w') as recipeFile:
        json.dump(recipeList, recipeFile, indent=4)

    return jsonify({'result': 'Successfully added'}), 201

# READ - GET
@app.route('/recipe', methods=["GET"])
def getRecipes():
    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())
    return jsonify(recipeList), 200

# UPDATE - PUT
@app.route('/updateRecipe', methods=["PUT"])
def updateRecipes():
    if 'name' not in request.json:
        return jsonify({'error': 'Missing fields'}), 422
    # get file contents and load them
    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())

    # Update
    for recipe in recipeList:
        if recipe["name"] == request.json["name"]:
            print('found it ', type(request.json.items()))
            for k in request.json:
                if (k.lower() in recipe) and (k.lower() != "name"):
                    recipe[k.lower()] = request.json[k]

    # write to json file
    with open('db-recipes.json','w') as recipeFile:
        json.dump(recipeList, recipeFile, indent=4)

    return jsonify(recipeList), 201

# DELETE - DELETE
@app.route('/badRecipe', methods=["DELETE"])
def deleteRecipes():
    # Validate Name
    name = request.args.get("name")
    if (name == "") or (name == None):
        return jsonify({'error': 'Missing fields'}), 422
    # Use varaible (optional) to indicate a successful
    found = False
    # get file contents and load them
    with open('db-recipes.json', 'r') as recipeFile:
        recipeList = json.loads(recipeFile.read())

    for r in recipeList:
        if r['name'] == name:
            found = True
            recipeList.remove(r)

    # write to json file
    with open('db-recipes.json','w') as recipeFile:
        json.dump(recipeList, recipeFile, indent=4)
    message = {"body": "Deleted!"} if found == True else {"body": "Cannot find record to delete"}
    return jsonify(message), 200

#BONUS - ERROR HANDLING
@app.errorhandler(404)
def not_found(error=None):
    return jsonify({'error': "Sorry, we don't recognize this URL!"}), 404

app.run()

# another way to design this wouldve been having receipe as the path for each
#and the difference would be just having the HTTP methods mapping to the
#appropiate route
