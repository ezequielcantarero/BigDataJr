from main import COLLECTION_NAME, DB_NAME, get_client

# 1. Obtenemos el cliente validado y la colección desde main.py
client = get_client()
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

print(
    f"Conexión exitosa. Documentos listos para consultar: {coleccion.count_documents({})}"
)

# ---------------------------------------------------------
# A. find(): Búsqueda con condición numérica y proyección
# ---------------------------------------------------------
print("\n--- 1. Publicaciones con más de 400 likes ---")
filtro = {"likes": {"$gt": 400}}
proyeccion = {"_id": 0, "usuario": 1, "likes": 1, "tags": 1}
#proyeccion: nos permite seleccionar los campos que queremos mostrar, es el equivalente a 
# select en sql. 0 no muestra y 1 muestra. Por defecto muestra todo.


for doc in coleccion.find(filtro, proyeccion).limit(5):
    print(doc)

# ---------------------------------------------------------
# B. sort(): Ordenar de mayor a menor por likes
# -1 = Descendente, 1 = Ascendente
# ---------------------------------------------------------
print("\n--- 2. Top 5 publicaciones con más likes ---")
top_likes = (
    coleccion.find({}, {"_id": 0, "usuario": 1, "likes": 1, "verificado": 1})
    .sort("likes", -1)
    .limit(5)
)

for puesto, doc in enumerate(top_likes, start=1):
    verif = "Verificado" if doc.get("verificado") else "No verificado"
    print(f"#{puesto}: {doc['usuario']} | {doc['likes']} likes | {verif}")

# ---------------------------------------------------------
# C. find() en arrays: Buscar dentro de la lista 'tags'
# ---------------------------------------------------------
print("\n--- 3. Publicaciones que contienen el tag 'bigdata' ---")
con_tag = coleccion.find(
    {"tags": "bigdata"}, {"_id": 0, "usuario": 1, "tags": 1}
).limit(3)

for doc in con_tag:
    print(f"Usuario: {doc['usuario']} | Tags: {doc['tags']}")

# ---------------------------------------------------------
# D. skip() y limit(): Paginación ordenada por fecha
# ---------------------------------------------------------
tamano_pagina = 3

print("\n--- 4. Paginación: Página 1 (Los 3 más recientes) ---")
pagina_1 = (
    coleccion.find({}, {"_id": 0, "usuario": 1, "fecha": 1, "likes": 1})
    .sort("fecha", -1)
    .skip(0)
    .limit(tamano_pagina)
)
for doc in pagina_1:
    print(
        f"Fecha: {doc['fecha'].strftime('%Y-%m-%d')} | Usuario: {doc['usuario']} | Likes: {doc['likes']}"
    )

print("\n--- 5. Paginación: Página 2 (Saltar 3 y traer los siguientes 3) ---")
pagina_2 = (
    coleccion.find({}, {"_id": 0, "usuario": 1, "fecha": 1, "likes": 1})
    .sort("fecha", -1)
    .skip(tamano_pagina)
    .limit(tamano_pagina)
)
for doc in pagina_2:
    print(
        f"Fecha: {doc['fecha'].strftime('%Y-%m-%d')} | Usuario: {doc['usuario']} | Likes: {doc['likes']}"
    )

# Cerramos la conexión
client.close()

"""
enumerate(iterable): Por defecto, empieza a contar desde 0 (daría puestos #0, #1, #2...).

    start=1: Le indica al contador que comience en 1 en lugar de 0. Así obtienes directamente un ranking natural (#1, #2, #3...) sin tener que escribir puesto + 1 manualmente.

3. Resumen de funciones utilizadas en MongoDB / PyMongo

    coleccion.find(filtro, proyeccion)

        Qué hace: Busca y recupera documentos de la colección. Devuelve un cursor iterable (no carga todo en memoria de golpe).

        Argumentos:

            filtro (opcional): Diccionario con las condiciones de búsqueda (ej. {"likes": {"$gt": 400}}). Si pasas {} o nada, trae todos.

            proyeccion (opcional): Diccionario que define qué campos devolver (ej. {"_id": 0, "usuario": 1}).

    cursor.sort(campo, direccion)

        Qué hace: Ordena los documentos resultantes antes de entregártelos.

        Argumentos:

            campo: Nombre del campo por el cual ordenar (ej. "likes").

            direccion: 1 para orden ascendente (menor a mayor / A-Z) o -1 para descendente (mayor a menor / Z-A).

    cursor.limit(n)

        Qué hace: Limita la cantidad máxima de documentos devueltos por el cursor.

        Argumentos:

            n: Número entero indicando el tope de registros a traer (ej. .limit(5) sólo entrega 5).

    cursor.skip(n)

        Qué hace: Salta o ignora los primeros n documentos del resultado antes de empezar a leer.

        Argumentos:

            n: Número entero con la cantidad de documentos a omitir. Combinado con limit() es la base para paginar (por ejemplo, página 2 salta los primeros registros con .skip(tamano_pagina)).

    coleccion.count_documents(filtro)

        Qué hace: Cuenta cuántos documentos coinciden con una condición sin necesidad de traerlos a Python.

        Argumentos:

            filtro: Diccionario con la condición. Si pasas {} cuenta el total absoluto de la colección.
"""