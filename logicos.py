import re
from main import COLLECTION_NAME, DB_NAME, get_client

client = get_client()
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

# ---------------------------------------------------------
# 1. Operadores de rango ($gte, $lte) y pertenencia ($in)
# ---------------------------------------------------------
# Documentos con likes entre 200 y 300 de ciertos usuarios específicos
print("--- 1. Rango numérico y lista de pertenencia ($in) ---")
filtro_rango = {
    "likes": {"$gte": 200, "$lte": 300},
    "usuario": {"$in": ["ana_dev", "lucas_ai"]},
}
proy = {"_id": 0, "usuario": 1, "likes": 1}

for doc in coleccion.find(filtro_rango, proy).limit(3):
    print(doc)

# ---------------------------------------------------------
# 2. Operador lógico $or
# ---------------------------------------------------------
# Publicaciones que sean de 'marta_cloud' O que tengan más de 450 likes
print("\n--- 2. Operador lógico $or ---")
filtro_or = {
    "$or": [
        {"usuario": "marta_cloud"},
        {"likes": {"$gt": 450}},
    ]
}

for doc in coleccion.find(filtro_or, {"_id": 0, "usuario": 1, "likes": 1}).limit(
    4
):
    print(doc)

# ---------------------------------------------------------
# 3. Consultas sobre arrays ($all y $size)
# ---------------------------------------------------------
# $all: el documento DEBE contener TODOS los elementos indicados
# $size: el array debe tener exactamente N elementos
print("\n--- 3. Arrays: $all y $size ---")
filtro_array = {
    "tags": {"$all": ["python", "bigdata"]},  # Debe incluir ambos tags
}
for doc in coleccion.find(filtro_array, {"_id": 0, "usuario": 1, "tags": 1}).limit(
    3
):
    print(f"Tags que contienen python y bigdata: {doc['tags']}")

filtro_tamano = {
    "tags": {"$size": 3}  # Publicaciones con exactamente 3 tags
}
total_con_3_tags = coleccion.count_documents(filtro_tamano)
print(f"Total de publicaciones con exactamente 3 tags: {total_con_3_tags}")

# ---------------------------------------------------------
# 4. Búsqueda de patrones de texto ($regex)
# ---------------------------------------------------------
# Buscar publicaciones cuyo contenido hable de 'rendimiento' o 'optimización'
print("\n--- 4. Búsqueda por expresión regular ($regex) ---")
filtro_regex = {
    "contenido": {
        "$regex": "rendimiento|optimizando",
        "$options": "i",
    }  # 'i' = case-insensitive
}
proy_texto = {"_id": 0, "usuario": 1, "contenido": 1}

for doc in coleccion.find(filtro_regex, proy_texto).limit(3):
    print(f"{doc['usuario']}: \"{doc['contenido']}\"")

client.close()

"""
Desglose de los nuevos operadores
    $gte y $lte: Greater than or equal ($\ge$) y Less than or equal ($\le$). Permiten definir rangos cerrados dentro de un mismo campo numérico o de fecha.
    $in: Recibe una lista ["val1", "val2"] y devuelve los documentos donde el campo coincida con cualquiera de esos valores (equivalente al IN (...) de SQL).
    $or: Recibe una lista de diccionarios de condiciones [condicion_1, condicion_2]. Si se cumple al menos una, el documento califica.
    $all: En campos tipo lista/array, verifica que existan todos los elementos especificados, sin importar el orden ni si hay otros elementos adicionales.
    $regex: Evalúa expresiones regulares sobre cadenas de texto. El parámetro "$options": "i" ignora mayúsculas y minúsculas (case-insensitive).
"""