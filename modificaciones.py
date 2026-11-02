from main import COLLECTION_NAME, DB_NAME, get_client

client = get_client()
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

# ---------------------------------------------------------
# 1. update_one con $set: Modificar un campo específico
# ---------------------------------------------------------
# Buscamos un documento de 'ana_dev' y cambiamos su estado a verificado
filtro = {"usuario": "ana_dev"}
cambio = {"$set": {"verificado": True, "perfil_activo": True}}

resultado_update = coleccion.update_one(filtro, cambio)
print(f"Coincidencias encontradas: {resultado_update.matched_count}")
print(f"Documentos modificados: {resultado_update.modified_count}")

# ---------------------------------------------------------
# 2. update_one con $inc: Incrementar o decrementar números
# ---------------------------------------------------------
# Simular que una publicación recibió 10 likes nuevos (+10)
# $inc suma el valor; si pasas un número negativo (-5), resta
resultado_inc = coleccion.update_one(
    {"usuario": "ana_dev"}, {"$inc": {"likes": 10}}
)
print(
    f"Likes incrementados en {resultado_inc.modified_count} documento(s)."
)

# ---------------------------------------------------------
# 3. Operaciones sobre arrays: $push y $pull
# ---------------------------------------------------------
# $push: Agrega un elemento nuevo a la lista 'tags'
coleccion.update_one(
    {"usuario": "ana_dev"}, {"$push": {"tags": "tutorial"}}
)

# $pull: Elimina un elemento específico de la lista 'tags'
coleccion.update_one(
    {"usuario": "ana_dev"}, {"$pull": {"tags": "streaming"}}
)

# Verificamos cómo quedó ese documento
doc_modificado = coleccion.find_one(
    {"usuario": "ana_dev"},
    {"_id": 0, "usuario": 1, "likes": 1, "tags": 1, "verificado": 1},
)
print(f"\nDocumento tras las modificaciones:\n{doc_modificado}")

# ---------------------------------------------------------
# 4. update_many: Modificar múltiples documentos a la vez
# ---------------------------------------------------------
# A todas las publicaciones con más de 450 likes les asignamos un nuevo campo 'destacado': True
resultado_masivo = coleccion.update_many(
    {"likes": {"$gt": 450}}, {"$set": {"destacado": True}}
)
print(
    f"\nPublicaciones marcadas como destacadas: {resultado_masivo.modified_count}"
)

# ---------------------------------------------------------
# 5. delete_one y delete_many: Eliminación
# ---------------------------------------------------------
# delete_one: Borra el primer documento que coincida con la condición
resultado_del_uno = coleccion.delete_one({"likes": 0})
print(
    f"\nPublicaciones con 0 likes eliminadas (máx 1): {resultado_del_uno.deleted_count}"
)

# delete_many: Borra todos los documentos que cumplan la condición
# (Ejemplo: borrar publicaciones con menos de 10 likes)
resultado_del_muchos = coleccion.delete_many({"likes": {"$lt": 10}})
print(
    f"Publicaciones con menos de 10 likes eliminadas: {resultado_del_muchos.deleted_count}"
)

print(
    f"\nTotal restante de documentos en la colección: {coleccion.count_documents({})}"
)

client.close()

"""
Resumen de los operadores de modificación

    $set: Agrega o actualiza campos sin alterar el resto del documento. Si el campo no existía previamente, MongoDB lo crea automáticamente.

    $inc: Incrementa de forma atómica campos numéricos (por ejemplo, contadores de visitas, likes o stock) sin riesgo de condiciones de carrera.

    $push: Inserta un elemento al final de un campo tipo array.

    $pull: Busca y elimina todas las apariciones de un valor dentro de un array.

    matched_count vs modified_count: El objeto retornado por update_one / update_many informa cuántos documentos cumplieron la condición (matched_count) y cuántos cambiaron efectivamente de valor (modified_count).
"""