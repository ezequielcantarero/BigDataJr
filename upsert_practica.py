from datetime import datetime
from pymongo import ReturnDocument
from main import COLLECTION_NAME, DB_NAME, get_client

client = get_client()
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

# ---------------------------------------------------------
# 1. Upsert cuando el documento NO existe (provoca un INSERT)
# ---------------------------------------------------------
print("--- 1. Upsert con inserción nueva ---")
filtro_nuevo = {"usuario": "nuevo_usuario_ai"}

operacion = {
    # $setOnInsert: solo se aplica si el documento se está creando desde cero
    "$setOnInsert": {
        "fecha_creacion": datetime.now(),
        "cuenta_origen": "sistema_auto",
    },
    # $set: se aplica SIEMPRE (tanto si se crea como si se actualiza)
    "$set": {"verificado": True, "contenido": "Mi primer documento generado."},
    # $inc: también se aplica siempre
    "$inc": {"visitas": 1},
}

resultado = coleccion.update_one(filtro_nuevo, operacion, upsert=True)

print(f"Coincidencias encontradas: {resultado.matched_count}")  # Será 0
print(f"Modificados: {resultado.modified_count}")  # Será 0
print(f"ID insertado por upsert: {resultado.upserted_id}")  # Trae el nuevo _id

# Verificamos cómo se guardó
doc_creado = coleccion.find_one({"_id": resultado.upserted_id})
print(f"Documento insertado:\n{doc_creado}\n")


# ---------------------------------------------------------
# 2. Upsert cuando el documento SÍ existe (provoca un UPDATE)
# ---------------------------------------------------------
print("--- 2. Upsert sobre documento existente ---")

operacion_update = {
    # $setOnInsert NO se ejecutará porque el documento ya existe
    "$setOnInsert": {"fecha_creacion": datetime(2000, 1, 1)},
    # $set actualizará el contenido
    "$set": {"contenido": "Contenido actualizado en segunda pasada."},
    # $inc sumará +1 a las visitas existentes
    "$inc": {"visitas": 1},
}

resultado_existente = coleccion.update_one(
    filtro_nuevo, operacion_update, upsert=True
)

print(
    f"Coincidencias encontradas: {resultado_existente.matched_count}"
)  # Será 1
print(f"Modificados: {resultado_existente.modified_count}")  # Será 1
print(
    f"ID de upsert: {resultado_existente.upserted_id}"
)  # Será None (no hubo insert)

# Comprobamos que 'fecha_creacion' mantuvo la fecha original y visitas subió a 2
doc_actualizado = coleccion.find_one(filtro_nuevo)
print(f"Documento tras update:\n{doc_actualizado}\n")


# ---------------------------------------------------------
# 3. find_one_and_update: Upsert atómico que devuelve el documento
# ---------------------------------------------------------
print("--- 3. find_one_and_update con upsert ---")

# En lugar de hacer update_one() y luego find_one() por separado,
# find_one_and_update hace ambas operaciones de forma atómica en un solo viaje de red.
doc_resultado = coleccion.find_one_and_update(
    {"usuario": "usuario_atomico"},
    {"$set": {"rol": "editor"}, "$inc": {"puntos": 50}},
    upsert=True,
    return_document=ReturnDocument.AFTER,  # Devuelve el documento DESPUÉS del cambio
)

print(f"Resultado directo de find_one_and_update:\n{doc_resultado}")

client.close()

"""
Puntos clave a recordar 

    upsert=True: Modifica el comportamiento por defecto de update_one y update_many. Si el filtro no arroja ningún documento, fusiona los criterios del filtro con los operadores del bloque de actualización para generar el nuevo registro.

    resultado.upserted_id: Si la operación insertó un nuevo registro, esta propiedad contiene el ObjectId asignado. Si actualizó un registro existente, su valor es None.

    $setOnInsert: Evita sobreescribir datos inmutables (marcas temporales de auditoría como created_at, claves fijas o valores por defecto).

    find_one_and_update: Imprescindible para colas de tareas, contadores de stock o reservas donde se necesita actualizar e inmediatamente leer el estado final sin peligro de que otro proceso interfiera entre el update y la consulta.
"""