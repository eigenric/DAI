from bson.json_util import dumps
from bson import ObjectId
from pymongo import MongoClient

from flask import Flask, Response, render_template, send_from_directory, jsonify, request, make_response
from ejercicios import fibonacci

app = Flask(__name__, static_url_path='/static')

client = MongoClient("mongo", 27017)

db = client.cockteles

@app.route("/api/recipes", methods=["GET", "POST"])
def api_1():
    if request.method == "GET": 
        lista = []
        buscados = db.recipes.find().sort("name")
        for recipe in buscados:
            recipe["_id"] = str(recipe["_id"])
            lista.append(recipe)
        app.logger.debug(lista)
        # Jsonify ya devuelve application json mimetype
        return jsonify(lista)

    if request.method == "POST": 
        # https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
        data = request.get_json()
        _id = db.recipes.insert_one(data)
        dict_id = { 
            "acknowledged": _id.acknowledged,
            "insertedId": str(_id.inserted_id)
        }
        data_created = db.recipes.find_one(_id.inserted_id)
        data_created["_id"] = str(_id.inserted_id)

        response = {
            "creation": dict_id, 
            "data": data_created
        }

        return jsonify(response), 201
    

# para devolver una, modificar o borrar
@app.route('/api/recipes/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_2(id):
    if request.method == 'GET':
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify(buscado), 404
        

@app.route("/api/recetas?con=<bebida>")
def api_recetas_con(bebida):
    buscado = db.recipes.find({"ingredients.name": {"$eq": f"{bebida}"}})
    if buscado:
        buscado['_id'] = str(buscado['_id'])
        return jsonify(buscado)
    else:
        return jsonify(buscado), 404
       
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

@app.route("/recetas_de/<bebida>")
def mongo_recetas_de(bebida):
    # Encontramos los documentos de la coleccion "recipes"
    bebida = bebida.replace("_", "-")
    app.logger.debug(bebida)
    recetas = db.recipes.find({"slug" : bebida}) # devuelve un cursor

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
    # TODO: Lemon Vodka es vodka (?)

    recetas_con_bebida = db.recipes.find({"ingredients.name": {"$eq": f"{bebida}"}})    

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
def recetas_n_ingredientes(n, field):

    if field not in ("ingredientes", "instrucciones"):
        return page_not_found()

    if field == "ingredientes":
        field = "ingredients"
    elif field == "instrucciones":
        field = "instructions"

    recetas_con_n_ingredients = db.recipes.aggregate([
        {"$match": {f"{field}": {"$size": n}}}
    ])

    lista_recetas = []
    for receta in recetas_con_n_ingredients:
        app.logger.debug(receta)
        lista_recetas.append(receta)
    
    response = {
        "len": len(lista_recetas),
        "data": lista_recetas
    }
    
    resJson = dumps(response)
    
    return Response(resJson, mimetype="application/json")

@app.route("/fibonacci/<int:n>")
def app_fibonacci(n):
    seq_n = fibonacci(n)
    return f"{seq_n}"

@app.route("/img")
def app_img():
    return send_from_directory("static", "cat.jpeg")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404