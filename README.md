# Desarrollo de Aplicaciones Para Internet

## Instalación

El proyecto archivo `docker-compose.yml` para la gestión de los 
contenedores y un archivo `Dockerfile` para el contenedor principal de
la aplicación (paquete app).

## Contenido

Primera entrega (P0-P2.2)

- **Práctica 0.** Configuración de entorno de trabajo. 
    - Docker y Docker-compose.
    - Introducción a Python.
        - Criba de Erastótenes
        - Secuencia de Fibonacci
        - Paréntesis Balanceados
        - Expresiones Regulares.
- **Práctica 1.** Introducción al Microframework Flask
    - Routing. /fibonacci/8
    - Servir Imágenes
    - Página de error 404.
- **Práctica 2.** Base de datos NoSQL MongoDB con Pymongo
    - Querys a la base de datos
    - `/recetas_de/cuba_libre`
    - `/recetas_con/vodka`
    - `/recetas_compuestas_de/<int:n>/ingredientes`
- **Práctica 2.2.** Desarrollo de API REST
    - Versión v1 Manual: app.py
    - Versión con Flask-RestFull: app2.py
        - Clases ListaReceta(Resource)
            - Método get
            - Método post
        - Clase Receta(Resource)
            - Método get
            - Método put
            - Método post
            - Método delete
        - Testeo de la API Restfull con extensión en VSCode.
- **Práctica 3.1** Uso de Django Web Framework
    - Instalación
    - Modelos `Receta` e `Ingrediente`
    - Url, views, django admin.
- **Práctica 3.2** Maquetación en plantillas django
    - Plantillas `base.html`, `index.html`, `receta.html`, y `search.html`
    - Uso de Boostrap Framework
    - Barra de navegación con cuadro de búsqueda (plantilla search)
    - Botón para modo oscuro
        - Uso de Boostrap-dark
        - Uso de Django sesiones (`session.theme` es `dark` `light`)
- **Práctica 3.3** Formularios
- **Práctica 3.4** Autentificación
- **Práctica 4** React:

