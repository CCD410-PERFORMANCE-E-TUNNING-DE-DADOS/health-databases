db = db.getSiblingDB('health');

db.createCollection('consultas');
db.createCollection('guias_atendimento');
db.createCollection('anamneses');
db.createCollection('prescricoes');
db.createCollection('resultados_exames');
db.createCollection('exames_solicitados');

db.consultas.createIndex({ paciente_id: 1 });
db.consultas.createIndex({ medico_id: 1 });
db.consultas.createIndex({ data_consulta: -1 });
db.consultas.createIndex({ cid10: 1 });

db.prescricoes.createIndex({ paciente_id: 1 });

db.resultados_exames.createIndex({ paciente_id: 1 });
db.resultados_exames.createIndex({ tipo_exame: 1 });

db.consultas.insertOne({
  paciente_id: "550e8400-e29b-41d4-a716-446655440000",
  medico_id: "550e8400-e29b-41d4-a716-446655440001",

  data_consulta: new Date("2025-03-10T14:30:00Z"),

  queixa_principal: "Dor abdominal persistente há 3 dias",

  transcricao:
    "Paciente relata dores na região epigástrica, piora após alimentação.",

  hipotese_diagnostica: "Gastrite aguda",

  cid10: "K29.7",

  prescricao: {
    medicamentos: [
      {
        nome: "Omeprazol",
        dose: "20mg",
        frequencia: "1x ao dia",
        duracao: "30 dias"
      }
    ],

    observacoes: "Evitar alimentos ácidos"
  },

  encaminhamentos: [],

  criado_em: new Date()
});

print("Banco health inicializado com sucesso.");
