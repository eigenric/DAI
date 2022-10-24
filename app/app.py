from bson.json_util import dumps
from pymongo import MongoClient

from flask import Flask, Response

app = Flask(__name__)

client = MongoClient("mongo", 27017)

db = client.cockteles


@app.route("/todas_las_recetas")
def mongo():
    # Encontramos los documentos de la coleccion "recipes"
    recetas = db.recipes.find() # devuelve un cursor

    lista_recetas = []
    for receta in recetas:
        app.logger.debug(receta) # salida consola
        lista_recetas.append(receta)

    response = {
        "len": len(lista_recetas),
        "data": lista_recetas
    } 

    resJson = dumps(response)

    return Response(resJson, mimetype="application/json")