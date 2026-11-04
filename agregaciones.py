from main import COLLECTION_NAME, DB_NAME, get_client

client = get_client()
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

# ---------------------------------------------------------
# 1. Agrupación simple: Métricas por usuario
# Objetivo: Por cada usuario, contar publicaciones, sumar likes y sacar promedio
# ---------------------------------------------------------
print("--- 1. Métricas de publicaciones por usuario ---")

pipeline_usuarios = [
    # Etapa 1: Solo tomar documentos que tengan el campo usuario
    {"$match": {"usuario": {"$exists": True, "$ne": None, "$type": "string"}}},
    # Etapa 2: Agrupar por el campo 'usuario'
    {
        "$group": {
            "_id": "$usuario",  # Campo por el que agrupamos (siempre va en _id)
            "total_publicaciones": {"$sum": 1},  # Cuenta 1 por cada documento
            "total_likes": {"$sum": "$likes"},  # Suma el campo 'likes'
            "promedio_likes": {"$avg": "$likes"},  # Promedio de likes
            "max_likes": {"$max": "$likes"},  # Publicación más viral
        }
    },
    # Etapa 3: Ordenar por promedio_likes de mayor a menor
    {"$sort": {"promedio_likes": -1}},
]

resultados_usuarios = coleccion.aggregate(pipeline_usuarios)

for r in resultados_usuarios:

    usuario_str = str(r["_id"]) if r["_id"] is not None else "Desconocido"
    promedio = r["promedio_likes"] if r["promedio_likes"] is not None else 0.0
    likes_totales = r["total_likes"] if r["total_likes"] is not None else 0
    maximo = r["max_likes"] if r["max_likes"] is not None else 0

    print(
        f"Usuario: {usuario_str:<15} | "
        f"Posts: {r['total_publicaciones']:<3} | "
        f"Likes Totales: {likes_totales:<6} | "
        f"Promedio: {promedio:.1f} | "
        f"Máx: {maximo}"
    )

# ---------------------------------------------------------
# 2. $unwind: Descomponer arrays para analizar tags
# Como 'tags' es una lista, $unwind separa cada tag en un documento individual
# ---------------------------------------------------------
print("\n--- 2. Top tags más utilizados y sus likes totales ---")

pipeline_tags = [
    {"$match": {"tags": {"$exists": True}}},
    # Desenrolla el array: si un doc tiene 3 tags, genera 3 documentos temporales
    {"$unwind": "$tags"},
    # Agrupamos por el tag individual
    {
        "$group": {
            "_id": "$tags",
            "veces_usado": {"$sum": 1},
            "likes_acumulados": {"$sum": "$likes"},
        }
    },
    # Ordenamos por cantidad de uso descendente
    {"$sort": {"veces_usado": -1}},
    # Opcional: renombrar y limpiar la salida
    {
        "$project": {
            "_id": 0,
            "tag": "$_id",
            "veces_usado": 1,
            "likes_acumulados": 1,
        }
    },
]

resultados_tags = coleccion.aggregate(pipeline_tags)

for tag_stat in resultados_tags:
    print(
        f"Tag: #{tag_stat['tag']:<16} | "
        f"Uso: {tag_stat['veces_usado']} veces | "
        f"Likes generados: {tag_stat['likes_acumulados']}"
    )

client.close()