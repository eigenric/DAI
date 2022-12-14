"""
Prácticas 0-2
"""

import json
from bson.json_util import dumps
from bson import ObjectId

from pymongo import MongoClient

from flask import (Flask, Response, render_template, send_from_directory, jsonify, 
                    request, make_response)
from ejercicios import fibonacci

app = Flask(__name__, static_url_path='/static')
client = MongoClient("mongo", 27017)
db = client.cockteles

# --- Práctica 1 --- Ejercicios

@app.route("/fibonacci/<int:n>")
def app_fibonacci(n):
    """Devolución del n-ésimo término de la sucesión de Fibonacci"""

    seq_n = fibonacci(n)
    return f"{seq_n}"

@app.route("/img")
def app_img():
    """Devolución de una imagen del directorio static"""

    return send_from_directory("static", "cat.jpeg")

@app.errorhandler(404)
def page_not_found(e):
    """Devolución de un Error 404"""

    return render_template('404.html'), 404

# --- Práctica 2.1 Búsquedas en MongoDB. ---

@app.route('/todas_las_recetas')
def mongo_todas_las_recetas():
    """Devuelve todas las recetas en formato json"""

    # Cursor(*) de recetas 
    recetas = db.recipes.find()

    lista_recetas = []
    for  receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    # Convertimos los resultados a formato JSON
    resJson = dumps(response)

    # Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json

    return Response(resJson, mimetype='application/json')

@app.route("/recetas_de/<cocktel>")
def mongo_recetas_de(cocktel):
    """Devuelve las recetas disponibles para cierto cocktel"""

    # Encontramos los documentos de la coleccion "recipes"

    cocktel = cocktel.replace("_", "-")
    app.logger.debug(cocktel)
    recetas = db.recipes.find({"slug" : cocktel}) # devuelve un cursor

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

@app.route("/recetas_con/<bebida>")
def mongo_recetas_con(bebida):
    """Devuelve las recetas con cierta bebida en sus ingredientes"""

    recetas_con_bebida = db.recipes.find({
        "ingredients.name": {"$eq": str(bebida) }
    } )    

    lista_recetas = []
    for receta in recetas_con_bebida:
        app.logger.debug(receta)
        lista_recetas.append(receta)

    response = {
        "len": len(lista_recetas),
        "data": lista_recetas
    }

    resJson = dumps(response)

    return Response(resJson, mimetype="application/json")

@app.route("/recetas_compuestas_de/<int:n>/<field>")
def mongo_recetas_n_ingredientes_o_instrucciones(n, field):
    """Devuelve las recetas compuestas de n ingredientes o instrucciones"""

    # Sólo pueden ser ingredientes o instrucciones.
    # En caso contrario enviamos 404
    if field not in ("ingredientes", "instrucciones"):
        return page_not_found()

    if field == "ingredientes":
        field = "ingredients"
    elif field == "instrucciones":
        field = "instructions"

    recetas_con_n_ingredientes = db.recipes.aggregate([
        {"$match": {f"{field}": {"$size": n}}}
    ])

    lista_recetas = [receta for receta in recetas_con_n_ingredientes]
    
    response = {
        "len": len(lista_recetas),
        "data": lista_recetas
    }
    resJson = dumps(response)
    return Response(resJson, mimetype="application/json")

# --- Práctica 2.2. API RESTFull -- 

class JSONEncoder(json.JSONEncoder):
    """Cast de objectID a Python str"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

@app.route("/api/recipes", methods=["GET", "POST"])
def api_recipes():
    """
        GET: Devolución de JSON con todas las recetas.
        POST: Crear recetas. Devuelve resultado y receta creada.
    """
    if request.method == "GET": 
        # Recetas con cierto ingrediente o todas las recetas
        if "con" in request.args:
            buscados = db.recipes.find({
                 "ingredients.name": {"$eq": "Vodka"} 
            })
        else: 
            buscados = db.recipes.find().sort("name")

        recetas = [str(receta) for receta in buscados]
        return jsonify(recetas), 200 # Ok

    elif request.method == "POST": 
        data = request.get_json()
        _id = db.recipes.insert_one(data)
        receta_creada = db.recipes.find_one(_id.inserted_id)
        return jsonify(receta_creada), 201 # Created


@app.route('/api/recipes/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_recipe(id):
    """
    GET: Devolver borrar una receta dado su id
    PUT: Modificar una receta dado su id
    DELETE: Borrar una receta dado su id
    """
    _id = {"_id": ObjectId(id)}

    if request.method ==  "GET":
        buscado = db.recipes.find_one(_id)
        if buscado:
            return jsonify(buscado), 200
        else:
            return jsonify({"message": "No se ha podido encontrar"}), 404

    elif request.method == "PUT":
        set_data = {"$set": request.get_json()}
        modificado = db.recipes.update_one(_id, set_data)

        if modificado.modified_count > 0:
            return jsonify({
                "message": "Modificado correctamente",
                **modificado.raw_result
            }), 200
        else:
            return jsonify({"message": "No se ha podido modificar"}), 404

    elif request.method == "DELETE":
        eliminado = db.recipes.delete_one(_id)
        if eliminado:
            return jsonify({
                "message": "Eliminado correctamente",
                **eliminado.raw_result
            }), 200
        else:
            return jsonify({"message": "No se ha podido eliminar"}), 404
