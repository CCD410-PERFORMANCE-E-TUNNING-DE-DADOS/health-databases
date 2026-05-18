from cassandra.cluster import Cluster
from faker import Faker

import uuid
import random
from datetime import datetime, timedelta

fake = Faker("pt_BR")

# =========================
# CONFIG
# =========================

NUM_LOGS_ACESSO = 300
NUM_LOGS_SISTEMA = 300
NUM_AUDITORIA = 300
NUM_FILAS = 300

# =========================
# CASSANDRA
# =========================

cluster = Cluster(["localhost"], port=9042)

session = cluster.connect("health_casdb")

# =========================
# HELPERS
# =========================

def rand_timestamp(days=30):
    return fake.date_time_between(
        start_date=f"-{days}d",
        end_date="now"
    )

def rand_date():
    return fake.date_between(
        start_date="-30d",
        end_date="today"
    )

# =========================
# logs_acesso
# =========================

acoes = [
    "LOGIN",
    "LOGOUT",
    "CRIAR_PACIENTE",
    "ATUALIZAR_CONSULTA",
    "VISUALIZAR_PRONTUARIO"
]

for _ in range(NUM_LOGS_ACESSO):

    funcionario_id = uuid.uuid4()

    data_evento = rand_date()

    timestamp_evento = rand_timestamp()

    acao = random.choice(acoes)

    ip_origem = fake.ipv4()

    detalhes = fake.sentence(nb_words=8)

    session.execute(
        """
        INSERT INTO logs_acesso (
            funcionario_id,
            data_evento,
            timestamp_evento,
            acao,
            ip_origem,
            detalhes
        )

        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            funcionario_id,
            data_evento,
            timestamp_evento,
            acao,
            ip_origem,
            detalhes
        )
    )

print("logs_acesso OK")

# =========================
# logs_sistema
# =========================

servicos = [
    "API",
    "AUTH",
    "MONGO",
    "POSTGRES",
    "CASSANDRA"
]

niveis = [
    "INFO",
    "WARN",
    "ERROR"
]

for _ in range(NUM_LOGS_SISTEMA):

    servico = random.choice(servicos)

    data_evento = rand_date()

    timestamp_evento = rand_timestamp()

    nivel = random.choice(niveis)

    mensagem = fake.sentence(nb_words=10)

    stacktrace = (
        fake.text(max_nb_chars=200)
        if nivel == "ERROR"
        else None
    )

    session.execute(
        """
        INSERT INTO logs_sistema (
            servico,
            data_evento,
            timestamp_evento,
            nivel,
            mensagem,
            stacktrace
        )

        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            servico,
            data_evento,
            timestamp_evento,
            nivel,
            mensagem,
            stacktrace
        )
    )

print("logs_sistema OK")

# =========================
# auditoria_dados
# =========================

entidades = [
    "PACIENTE",
    "CONSULTA",
    "FUNCIONARIO",
    "PRESCRICAO"
]

campos = [
    "telefone",
    "email",
    "statusconsulta",
    "logradouro"
]

for _ in range(NUM_AUDITORIA):

    data_evento = rand_date()

    timestamp_evento = rand_timestamp()

    entidade = random.choice(entidades)

    entidade_id = uuid.uuid4()

    usuario_id = uuid.uuid4()

    campo_alterado = random.choice(campos)

    valor_antigo = fake.word()

    valor_novo = fake.word()

    session.execute(
        """
        INSERT INTO auditoria_dados (
            data_evento,
            timestamp_evento,
            entidade,
            entidade_id,
            usuario_id,
            campo_alterado,
            valor_antigo,
            valor_novo
        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data_evento,
            timestamp_evento,
            entidade,
            entidade_id,
            usuario_id,
            campo_alterado,
            valor_antigo,
            valor_novo
        )
    )

print("auditoria_dados OK")

# =========================
# filas_atendimento
# =========================

setores = [
    "TRIAGEM",
    "CARDIOLOGIA",
    "PEDIATRIA",
    "ORTOPEDIA"
]

status_list = [
    "AGUARDANDO",
    "EM_ATENDIMENTO",
    "FINALIZADO"
]

prioridades = [
    "BAIXA",
    "MEDIA",
    "ALTA"
]

for _ in range(NUM_FILAS):

    setor = random.choice(setores)

    data_evento = rand_date()

    timestamp_evento = rand_timestamp()

    paciente_id = uuid.uuid4()

    status = random.choice(status_list)

    prioridade = random.choice(prioridades)

    session.execute(
        """
        INSERT INTO filas_atendimento (
            setor,
            data_evento,
            timestamp_evento,
            paciente_id,
            status,
            prioridade
        )

        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            setor,
            data_evento,
            timestamp_evento,
            paciente_id,
            status,
            prioridade
        )
    )

print("filas_atendimento OK")

# =========================
# DONE
# =========================

cluster.shutdown()

print("\nBanco Cassandra populado com sucesso!")
