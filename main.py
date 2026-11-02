from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bigdata_jr"
COLLECTION_NAME = "usuarios"


def get_client(uri: str = MONGO_URI) -> MongoClient:
    """Crea el cliente y verifica la conexión."""
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        client.admin.command("ping")
    except ConnectionFailure as e:
        raise SystemExit(f"No se pudo conectar a MongoDB: {e}")
    return client


def main():
    client = get_client()
    print("Conexión exitosa a MongoDB")

    # MongoDB crea la base de datos y la colección al insertar el primer documento
    db = client[DB_NAME]
    coleccion = db[COLLECTION_NAME]

    resultado = coleccion.insert_one({"nombre": "Ezequiel", "rol": "admin"})
    print(f"Documento insertado con _id: {resultado.inserted_id}")

    print("Bases de datos disponibles:", client.list_database_names())
    print("Documentos en la colección:")
    for doc in coleccion.find():
        print(doc)

    client.close()


if __name__ == "__main__":
    main()
