db = db.getSiblingDB('health_db');

db.createCollection('consultas');
db.createCollection('anamneses');

db.consultas.createIndex({ paciente_id: 1 });
db.consultas.createIndex({ medico_id: 1 });
db.consultas.createIndex({ data_consulta: -1 });
db.consultas.createIndex({ cid10: 1 });

print("Banco health inicializado com sucesso.");
