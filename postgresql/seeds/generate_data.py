from faker import Faker
import random

fake = Faker("pt_BR")

NUM_PESSOAS = 60
NUM_FUNCIONARIOS = 25
NUM_PACIENTES = 35
NUM_CONSULTAS = 60

sql = []

# ======================
# Helpers
# ======================
def clean(s):
    return str(s).replace("'", "''")

def telefone_br():
    return f"({random.randint(11,99)})9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def cep_br():
    return f"{random.randint(10000,99999)}-{random.randint(100,999)}"

def complemento_br():
    tipos = ["Apto", "Bloco", "Casa", "Fundos", "Sala"]
    return f"{random.choice(tipos)} {random.randint(1,999)}"

def tipo_sanguineo():
    return random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

def rand_bool():
    return random.choice(['true', 'false'])

def crm():
    return f"CRM-{random.randint(100000,999999)}/{fake.estado_sigla()}"

def coren():
    return f"COREN-{random.randint(100000,999999)}"

# ======================
# Pessoa
# ======================
cpfs = set()
pessoas = []

for i in range(1, NUM_PESSOAS + 1):

    cpf = fake.cpf().replace(".", "").replace("-", "")
    while cpf in cpfs:
        cpf = fake.cpf().replace(".", "").replace("-", "")
    cpfs.add(cpf)

    pessoa = {
        "id": i,
        "cpf": cpf,
        "nome": clean(fake.name()),
        "data": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "telefone": telefone_br(),
        "cep": cep_br(),
        "cidade": clean(fake.city()),
        "uf": fake.estado_sigla(),
        "logradouro": clean(fake.street_name()),
        "numero": str(random.randint(1, 999)),
        "complemento": clean(complemento_br())
    }

    pessoas.append(pessoa)

    sql.append(f"""
INSERT INTO ccd410.pessoa
(cpf, nome, dtNascimento, telefone, cep, cidade, uf, logradouro, numLogradouro, complemento)
VALUES
('{pessoa["cpf"]}', '{pessoa["nome"]}', '{pessoa["data"]}', '{pessoa["telefone"]}',
 '{pessoa["cep"]}', '{pessoa["cidade"]}', '{pessoa["uf"]}',
 '{pessoa["logradouro"]}', '{pessoa["numero"]}', '{pessoa["complemento"]}');
""")

# ======================
# Funcionarios
# ======================
funcionarios = []

for i in range(1, NUM_FUNCIONARIOS + 1):
    pessoa = pessoas[i - 1]

    funcionarios.append(i)

    sql.append(f"""
INSERT INTO ccd410.funcionario
(login, senha, statusFuncionario, dtContratacao, pessoaID)
VALUES
('user{i}', 'senha{122 + i}', 'ATIVO',
 '{fake.date_between(start_date="-10y")}', {pessoa["id"]});
""")

# ======================
# Pacientes
# ======================
pacientes = []

for i in range(1, NUM_PACIENTES + 1):
    pessoa = pessoas[NUM_FUNCIONARIOS + i - 1]
    pacientes.append(i)

    sql.append(f"""
INSERT INTO ccd410.paciente
(planoDeSaude, numCarteiraPlano, tipoSanguineo, pessoaID)
VALUES
('{clean(fake.company())}', '{fake.numerify("##########")}',
 '{tipo_sanguineo()}', {pessoa["id"]});
""")

# ======================
# Profissões
# ======================
medicos = random.sample(funcionarios, k=10)
restantes = [f for f in funcionarios if f not in medicos]

enfermeiros = random.sample(restantes, k=8)
recepcionistas = [f for f in restantes if f not in enfermeiros]

# Medicos
especialidades = [
    "Cardiologia", "Pediatria", "Ortopedia", "Dermatologia",
    "Neurologia", "Clínico Geral"
]

for f in medicos:
    sql.append(f"""
INSERT INTO ccd410.medico
(funcionarioID, especialidade, crm)
VALUES
({f}, '{random.choice(especialidades)}', '{crm()}');
""")

# Enfermeiros
for f in enfermeiros:
    sql.append(f"""
INSERT INTO ccd410.enfermeiro
(funcionarioID, coren)
VALUES
({f}, '{coren()}');
""")

# Recepcionistas
for f in recepcionistas:
    sql.append(f"""
INSERT INTO ccd410.recepcionista
(funcionarioID, setor, ramal, telefoneProfissional)
VALUES
({f}, '{clean(fake.word())}', {random.randint(1000,9999)},
 '{telefone_br()}');
""")

# ======================
# Consultas
# ======================
consultas = []

for i in range(1, NUM_CONSULTAS + 1):
    paciente = random.choice(pacientes)
    medico = random.choice(medicos)

    consultas.append(i)

    sql.append(f"""
INSERT INTO ccd410.consulta
(dtConsulta, retorno, descricao, encaminhamento, pacienteID, funcionarioID)
VALUES
('{fake.date_between(start_date="-1y")}', {rand_bool()},
 '{clean(fake.sentence(nb_words=10))}',
 '{clean(fake.word())}',
 {paciente}, {medico});
""")

# ======================
# Alergias
# ======================
alergias_comuns = ["Lactose", "Glúten", "Pólen", "Amendoim", "Frutos do mar"]

for i in range(30):
    sql.append(f"""
INSERT INTO ccd410.alergias
(descricao, pacienteID)
VALUES
('{random.choice(alergias_comuns)}', {random.choice(pacientes)});
""")

# ======================
# Remédios
# ======================
remedios = ["Dipirona", "Paracetamol", "Ibuprofeno", "Amoxicilina"]

for i in range(30):
    sql.append(f"""
INSERT INTO ccd410.remedios_recorrentes
(descricao, pacienteID)
VALUES
('{random.choice(remedios)}', {random.choice(pacientes)});
""")

# ======================
# Exames
# ======================
exames = ["Hemograma", "Raio-X", "Ressonância", "Tomografia", "Ultrassom"]

for i in range(40):
    sql.append(f"""
INSERT INTO ccd410.exames_solicitados
(nome, especialidade, descricao, resultado, consultaID)
VALUES
('{random.choice(exames)}',
 '{random.choice(especialidades)}',
 '{clean(fake.sentence())}',
 '{clean(fake.word())}',
 {random.choice(consultas)});
""")

# ======================
# Salvar arquivo
# ======================
with open("populate_tables.sql", "w") as f:
    f.write("\n".join(sql))

print("populate_tables.sql gerado com sucesso!")
