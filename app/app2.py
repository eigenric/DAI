""" Segunda versión utilizado Flask RestFull """

import json
from bson import ObjectId
from datetime import datetime
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongo", 27017)
db = client.cockteles

recipes_args = reqparse.RequestParser()
recipes_args.add_argument("con", type=str, help="Recetas con cierto ingrediente")

class JSONEncoder(json.JSONEncoder):
    """Cast de ObjectId a Python str"""

    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

class Recipes(Resource):
    def get(self):
        if "con" in request.args:
            # Recetas con cualquier ingrediente que
            # contenga la palabra Vodka (Case insensitive)
            buscados = db.recipes.find({
                 "ingredients.name": { 
                    "$regex": "Vodka",
                    "$options": "i"
                } 
            })
        else: 
            buscados = db.recipes.find().sort("name")
        return jsonify(list(buscados))

    def post(self):
        data = request.get_json()
        _id = db.recipes.insert_one(data)
        receta_creada = db.recipes.find_one(_id.inserted_id)
        return jsonify(receta_creada)

recipe_put_args = reqparse.RequestParser()

class Recipe(Resource):

    def _abort_if_not_found(self, id):
        buscado = db.recipes.find_one(id)
        if not buscado:
            abort(404, message="No se ha podido encontrar la receta")

    def get(self, recipe_id):
        id = {"_id": ObjectId(recipe_id)}
        buscado = db.recipes.find_one(id)
        if buscado:
            return jsonify(buscado)
        else:
            return abort(404, message="No se ha podido encontrar la receta...")

    def put(self, recipe_id):
        id = {"_id": ObjectId(recipe_id)}
        self._abort_if_not_found(id)

        set_data = {"$set": request.get_json()}
        modificado = db.recipes.update_one(id, set_data)

        if modificado.modified_count > 0:
            receta = db.recipes.find_one(ObjectId(recipe_id))
            return jsonify(receta)
        else:
            return abort(404, message="No se ha modificado la receta")

    def delete(self, recipe_id):
        id = {"_id": ObjectId(recipe_id)}
        self._abort_if_not_found(id)

        eliminado = db.recipes.delete_one(id)
        if eliminado.acknowledged:
            return None, 204


api.add_resource(Recipe, "/api/recipes/<string:recipe_id>")
api.add_resource(Recipes, "/api/recipes/")