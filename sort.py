from pymongo import ReturnDocument, ASCENDING, DESCENDING
from main import COLLECTION_NAME, DB_NAME, get_client

client = get_client()
db = client[DB_NAME]
coleccion = db[COLLECTION_NAME]

# Caso: De todas las publicaciones no verificadas, premiar a la que tenga MÁS likes
doc_premiado = coleccion.find_one_and_update(
    filter={"verificado": False},
    update={"$set": {"verificado": True, "destacado": True}},
    sort=[("likes", -1)],  # -1 = Mayor a menor: elige el de mayor likes
    return_document=ReturnDocument.AFTER,
)

print(
    f"Usuario premiado: {doc_premiado['usuario']} con {doc_premiado['likes']} likes."
)

# Caso tipo cola de tareas: Tomar la publicación MÁS ANTIGUA para procesarla
doc_antiguo = coleccion.find_one_and_update(
    filter={"procesado": {"$exists": False}, 
            "fecha": {"$exists": True},
            },
    update={"$set": {"procesado": True}},
    sort=[("fecha", 1)],  # 1 = Ascendente: la fecha más vieja va primero
    return_document=ReturnDocument.AFTER,
)

if doc_antiguo:
    print(
        f"Publicación más vieja procesada: fecha {doc_antiguo['fecha'].strftime('%Y-%m-%d')}"
    )

# Ordenar por:
# 1. 'usuario' de forma ascendente (A -> Z)
# 2. 'likes' de forma descendente (del que más tiene al que menos)
cursor = (
    coleccion.find(
        {},
        {
            "_id": 0,
            "usuario": 1,
            "likes": 1,
            "fecha": 1,
        },
    )
    .sort([("usuario", 1), ("likes", -1)])
    .limit(8)
)

print("\n--- Orden múltiple: Usuario (A-Z) y luego Likes (Descendente) ---")
for doc in cursor:
    print(f"Usuario: {doc['usuario']:<15} | Likes: {doc['likes']}")

client.close()