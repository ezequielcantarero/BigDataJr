import random
from datetime import datetime, timedelta
from pymongo import MongoClient

# 1. Conexión al servidor local de MongoDB
cliente = MongoClient("mongodb://localhost:27017/")

# 2. Creación / selección de base de datos y colección
db = cliente["bigdata_jr"]
coleccion = db["usuarios"]

# Limpiamos la colección por si ejecutamos varias veces
coleccion.delete_many({})

# 3. Listas base para generar contenido aleatorio
usuarios = ["ana_dev", "carlos_data", "sofia_tech", "lucas_ai", "marta_cloud"]
temas = ["python", "mongodb", "bigdata", "streaming", "machinelearning"]
mensajes_base = [
    "Aprendiendo a estructurar colecciones NoSQL.",
    "Comparando rendimiento de consultas en bases documentales.",
    "Optimizando agregaciones con índices.",
    "Primeros pasos procesando flujos de datos.",
    "Documentos embebidos vs referencias en BSON.",
]

# 4. Generación e inserción de documentos aleatorios
documentos = []
fecha_base = datetime.now()

for i in range(500):  # Generamos 100 documentos para poder paginar
    doc = {
        "usuario": random.choice(usuarios),
        "contenido": random.choice(mensajes_base),
        "tags": random.sample(temas, k=random.randint(1, 3)),
        "likes": random.randint(0, 500),
        "compartidos": random.randint(0, 100),
        "fecha": fecha_base - timedelta(days=random.randint(0, 30)),
        "verificado": random.choice([True, False]),
    }
    documentos.append(doc)

# Inserción masiva (equivalente a insert_many)
resultado = coleccion.insert_many(documentos)
print(f"Insertados exitosamente {len(resultado.inserted_ids)} documentos.")