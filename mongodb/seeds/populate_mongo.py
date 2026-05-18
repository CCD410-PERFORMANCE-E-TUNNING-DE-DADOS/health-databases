from pymongo import MongoClient
from faker import Faker

import random
import uuid
from datetime import datetime, timedelta

fake = Faker("pt_BR")

# =========================
# CONFIG
# =========================

MONGO_USER = "health_user"
MONGO_PASSWORD = "health_pass"
MONGO_HOST = "mongodb"
MONGO_PORT = 27017
MONGO_DB = "health_db"

NUM_CONSULTAS = 200
NUM_ANAMNESES = 100
NUM_PRESCRICOES = 100
NUM_RESULTADOS = 100

# =========================
# CONEXAO
# =========================

uri = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@{MONGO_HOST}:{MONGO_PORT}/"
    f"{MONGO_DB}?authSource=admin"
)

client = MongoClient(uri)

db = client[MONGO_DB]

print("Conectado ao MongoDB")

# =========================
# HELPERS
# =========================

def random_date():
    return fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

def cid10():
    return random.choice([
        "K29.7",
        "J11",
        "M54.5",
        "I10",
        "E11",
        "A09"
    ])

def medicamento():
    meds = [
        "Omeprazol",
        "Dipirona",
        "Amoxicilina",
        "Ibuprofeno",
        "Losartana",
        "Paracetamol"
    ]

    return {
        "nome": random.choice(meds),
        "dose": random.choice([
            "10mg",
            "20mg",
            "500mg",
            "1g"
        ]),
        "frequencia": random.choice([
            "1x ao dia",
            "2x ao dia",
            "8/8h"
        ]),
        "duracao": random.choice([
            "5 dias",
            "7 dias",
            "30 dias"
        ])
    }

# =========================
# CONSULTAS
# =========================

consultas = []

for _ in range(NUM_CONSULTAS):

    consulta = {

        "paciente_id": str(uuid.uuid4()),

        "medico_id": str(uuid.uuid4()),

        "data_consulta": random_date(),

        "queixa_principal": fake.sentence(nb_words=8),

        "transcricao": fake.text(max_nb_chars=1000),

        "hipotese_diagnostica": fake.sentence(nb_words=4),

        "cid10": cid10(),

        "prescricao": {

            "medicamentos": [
                medicamento()
                for _ in range(random.randint(1, 3))
            ],

            "observacoes": fake.sentence(nb_words=10)
        },

        "encaminhamentos": [
            fake.word()
            for _ in range(random.randint(0, 3))
        ]
    }

    consultas.append(consulta)

db.consultas.insert_many(consultas)

print(f"{NUM_CONSULTAS} consultas inseridas")

# =========================
# ANAMNESES
# =========================

anamneses = []

for _ in range(NUM_ANAMNESES):

    anamneses.append({

        "paciente_id": str(uuid.uuid4()),

        "data_triagem": random_date(),

        "peso": round(random.uniform(45, 120), 1),

        "altura": round(random.uniform(1.45, 2.0), 2),

        "pressao_arterial": f"{random.randint(10,14)}/{random.randint(6,9)}",

        "temperatura": round(random.uniform(35.5, 39.5), 1),

        "alergias": [
            fake.word()
            for _ in range(random.randint(0, 3))
        ],

        "remedios_recorrentes": [
            fake.word()
            for _ in range(random.randint(0, 3))
        ],

        "observacoes": fake.text(max_nb_chars=300)
    })

db.anamneses.insert_many(anamneses)

print(f"{NUM_ANAMNESES} anamneses inseridas")

# =========================
# PRESCRICOES
# =========================

prescricoes = []

for _ in range(NUM_PRESCRICOES):

    prescricoes.append({

        "consulta_id": str(uuid.uuid4()),

        "paciente_id": str(uuid.uuid4()),

        "medico_id": str(uuid.uuid4()),

        "data_prescricao": random_date(),

        "medicamentos": [
            medicamento()
            for _ in range(random.randint(1, 4))
        ],

        "observacoes": fake.sentence(nb_words=12)
    })

db.prescricoes.insert_many(prescricoes)

print(f"{NUM_PRESCRICOES} prescricoes inseridas")

# =========================
# RESULTADOS EXAMES
# =========================

resultados = []

for _ in range(NUM_RESULTADOS):

    resultados.append({

        "paciente_id": str(uuid.uuid4()),

        "tipo_exame": random.choice([
            "Hemograma",
            "Raio-X",
            "Tomografia",
            "Ressonância",
            "Ultrassom"
        ]),

        "data_exame": random_date(),

        "resultado": fake.text(max_nb_chars=500),

        "arquivo_url": fake.url(),

        "medico_responsavel": fake.name()
    })

db.resultados_exames.insert_many(resultados)

print(f"{NUM_RESULTADOS} resultados_exames inseridos")

# =========================
# FINAL
# =========================

print("\nMongoDB populado com sucesso.")
