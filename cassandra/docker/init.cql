CREATE KEYSPACE IF NOT EXISTS health_casdb
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

USE health_casdb;


CREATE TABLE IF NOT EXISTS logs_acesso (
    funcionario_id INT,
    data_evento DATE,
    timestamp_evento TIMESTAMP,
    acao TEXT,
    ip_origem TEXT,
    detalhes TEXT,

    PRIMARY KEY (
        (funcionario_id, data_evento),
        timestamp_evento
    )
)
WITH CLUSTERING ORDER BY (timestamp_evento DESC);


CREATE TABLE IF NOT EXISTS logs_sistema (
    servico TEXT,
    data_evento DATE,
    timestamp_evento TIMESTAMP,
    nivel TEXT,
    mensagem TEXT,
    stacktrace TEXT,

    PRIMARY KEY (
        (servico, data_evento),
        timestamp_evento
    )
)
WITH CLUSTERING ORDER BY (timestamp_evento DESC)
AND compaction = {
    'class': 'TimeWindowCompactionStrategy'
};


CREATE TABLE IF NOT EXISTS auditoria_dados (
    timestamp_evento TIMESTAMP,
    data_evento DATE,    
    entidade TEXT,
    funcionario_id INT,
    campo_alterado TEXT,
    valor_antigo TEXT,
    valor_novo TEXT,

    PRIMARY KEY (
        (funcionario_id,data_evento),
        timestamp_evento
    )
)
WITH CLUSTERING ORDER BY (timestamp_evento DESC);
