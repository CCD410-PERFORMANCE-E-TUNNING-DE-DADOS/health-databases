# 📋 PRP — Project Requirements Plan

> **Sistema Hospitalar Centralizado com Integração Poliglota de Bancos de Dados**

---

## Sumário

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Objetivos](#2-objetivos)
3. [Justificativa Técnica — Teorema CAP](#3-justificativa-técnica--teorema-cap)
4. [Arquitetura dos Bancos de Dados](#4-arquitetura-dos-bancos-de-dados)
5. [Entidades e Responsabilidades](#5-entidades-e-responsabilidades)
6. [Controle de Acesso por Perfil](#6-controle-de-acesso-por-perfil)
7. [Requisitos Funcionais](#7-requisitos-funcionais)
8. [Requisitos Não Funcionais](#8-requisitos-não-funcionais)
9. [Diagrama de Responsabilidades dos Bancos](#9-diagrama-de-responsabilidades-dos-bancos)
10. [Estrutura Sugerida do Repositório](#10-estrutura-sugerida-do-repositório)
11. [Tecnologias e Stack](#11-tecnologias-e-stack)

---

## 1. Visão Geral do Projeto

Este projeto acadêmico tem como proposta o desenvolvimento de um **sistema hospitalar centralizado** com foco em **persistência poliglota** (*polyglot persistence*), ou seja, a utilização de múltiplos bancos de dados distintos de forma integrada, cada um sendo explorado segundo suas capacidades naturais.

A proposta explora, na prática, as garantias e trade-offs descritos pelo **Teorema CAP** (Consistency, Availability, Partition Tolerance), utilizando três bancos de dados com perfis complementares:

| Banco        | Perfil CAP           | Papel no Sistema                    |
|--------------|----------------------|-------------------------------------|
| PostgreSQL   | CP — Consistência    | Dados relacionais e estruturados    |
| MongoDB      | AP — Disponibilidade | Documentos clínicos não relacionais |
| Cassandra    | AP — Partição        | Logs, eventos e dados temporais     |

---

## 2. Objetivos

### 2.1 Objetivo Geral

Desenvolver um sistema de gestão hospitalar que integre três paradigmas distintos de banco de dados, demonstrando na prática como diferentes modelos de dados se complementam para atender cenários reais de alta complexidade.

### 2.2 Objetivos Específicos

- Modelar e implementar o esquema relacional no **PostgreSQL** para dados críticos e estruturados.
- Utilizar o **MongoDB** para armazenamento de documentos clínicos semi-estruturados e de alta variabilidade.
- Explorar o **Cassandra** para ingestão de grandes volumes de logs e eventos com alta disponibilidade e escalabilidade horizontal.
- Implementar uma camada de integração (API ou serviço) que orquestre os três bancos de forma transparente.
- Demonstrar, por meio de exemplos concretos, os trade-offs de cada banco segundo o Teorema CAP.

---

## 3. Justificativa Técnica — Teorema CAP

O **Teorema CAP**, enunciado por Eric Brewer, afirma que sistemas distribuídos só podem garantir simultaneamente **dois** dos três atributos abaixo:

```
C — Consistency (Consistência):       todos os nós veem os mesmos dados ao mesmo tempo
A — Availability (Disponibilidade):   toda requisição recebe uma resposta (sem garantia de atualidade)
P — Partition Tolerance (Partição):   o sistema continua operando mesmo com falhas de rede
```

A escolha dos três bancos foi deliberadamente feita para cobrir os três vértices do triângulo CAP:

```
            [C] Consistência
               /\
              /  \
        CP   /    \  CP+AP
            /      \
           /________\
     [P] Partição   [A] Disponibilidade
          AP              AP
```

| Banco      | Garantias Priorizadas | Justificativa de Uso                                                                                 |
|------------|-----------------------|------------------------------------------------------------------------------------------------------|
| PostgreSQL | **C + P**             | Dados de pacientes e funcionários exigem consistência forte e integridade referencial  		    |
| MongoDB    | **A + P**             | Documentos de consulta variam em estrutura; disponibilidade é mais crítica que consistência imediata |
| Cassandra  | **A + P**             | Logs e eventos são gerados em alto volume; consistência eventual é aceitável          		    |

---

## 4. Arquitetura dos Bancos de Dados

### 4.1 PostgreSQL — Consistência e Dados Relacionais

**Papel:** Núcleo relacional do sistema. Armazena os dados mais críticos e estruturados, onde a integridade referencial é essencial.

**Entidades principais:**

- `pacientes` — dados cadastrais/sensíveis (nome, CPF, data de nascimento, contato, endereço)
- `funcionarios` — dados dos profissionais (nome, CRM/COREN/CPF, cargo, setor)
- `consulta` — consultas agendadas, com referências a paciente, médico e sala, e tabela de referência cruzada apontando para documentos no MongoDB

**Características exploradas:**
- Transações ACID
- Chaves estrangeiras e integridade referencial
- Índices compostos para consultas otimizadas
- Views e procedures para relatórios

---

### 4.2 MongoDB — Disponibilidade e Documentos Clínicos

**Papel:** Armazenamento de documentos clínicos ricos e de estrutura variável, onde a flexibilidade do schema é uma vantagem real.

**Coleções principais:**

- `consultas` — transcrições e resumos de consultas médicas (texto livre, anexos, CID-10)
- `guias_atendimento` — solicitações de exames, guias de encaminhamento, autorizações
- `anamneses` — histórico clínico detalhado preenchido durante a triagem
- `prescricoes` — prescrições médicas com medicamentos, dosagens e observações
- `resultados_exames` — resultados de exames laboratoriais e de imagem (incluindo referências a arquivos)

**Exemplo de documento `consultas`:**

```json
{
  "_id": "ObjectId(...)",
  "paciente_id": "UUID do PostgreSQL",
  "medico_id": "UUID do PostgreSQL",
  "data_consulta": "2025-03-10T14:30:00Z",
  "queixa_principal": "Dor abdominal persistente há 3 dias",
  "transcricao": "Paciente relata...",
  "hipotese_diagnostica": "Gastrite aguda",
  "cid10": "K29.7",
  "prescricao": {
    "medicamentos": [
      { "nome": "Omeprazol", "dose": "20mg", "frequencia": "1x ao dia", "duracao": "30 dias" }
    ],
    "observacoes": "Evitar alimentos ácidos"
  },
  "encaminhamentos": []
}
```

**Características exploradas:**
- Schema flexível (documentos embarcados)
- Consultas por campos aninhados
- Aggregation pipeline para relatórios clínicos
- Referências cruzadas com IDs do PostgreSQL

---

### 4.3 Cassandra — Partição e Dados de Alta Volumetria

**Papel:** Ingestão e consulta de grandes volumes de dados temporais, logs de sistema e eventos de monitoramento, onde a escalabilidade horizontal e a alta disponibilidade são prioritárias.

**Tabelas principais (column families):**

- `logs_acesso` — registro de cada login/logout e operação realizada por funcionários
- `logs_sistema` — eventos técnicos da aplicação (erros, warnings, métricas)
- `eventos_vitais` — sinais vitais de pacientes internados coletados em intervalos regulares (pressão, temperatura, SpO2, frequência cardíaca)
- `auditoria_dados` — rastreio de alterações em registros críticos (quem alterou, quando, valor anterior vs. novo)
- `filas_atendimento` — histórico de estados da fila de espera por setor/data

**Exemplo de modelo `eventos_vitais`:**

```cql
CREATE TABLE eventos_vitais (
  paciente_id     UUID,
  internacao_id   UUID,
  coletado_em     TIMESTAMP,
  pressao_sistol  INT,
  pressao_diast   INT,
  temperatura     DECIMAL,
  spo2            INT,
  freq_cardiaca   INT,
  coletado_por    UUID,
  PRIMARY KEY ((paciente_id, internacao_id), coletado_em)
) WITH CLUSTERING ORDER BY (coletado_em DESC);
```

**Características exploradas:**
- Modelagem orientada a queries (query-first design)
- Partition key para distribuição de dados
- Clustering columns para ordenação temporal
- Compaction strategies para dados de séries temporais
- Consistência eventual configurável (`QUORUM`, `ONE`, `ALL`)

---

## 5. Entidades e Responsabilidades

```
┌─────────────────────────────────────────────────────────────┐
│                        PostgreSQL                           │
│                                                             │
│  pacientes ──────────────────── funcionarios                │
│      │                                │                     │
│      ├── internacoes                  ├── perfis_acesso     │
│      ├── agendamentos                 └── setores           │
│      └── prontuario_ref ──────────────────────────────┐     │
└───────────────────────────────────────────────────────┼─────┘
                                                        │ referencia
┌───────────────────────────────────────────────────────┼─────┐
│                        MongoDB                        │     │
│                                                       │     │
│  consultas ◄──────────────────────────────────────────┘     │
│  guias_atendimento                                          │
│  anamneses                                                  │
│  prescricoes                                                │
│  resultados_exames                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        Cassandra                            │
│                                                             │
│  logs_acesso          auditoria_dados                       │
│  logs_sistema         filas_atendimento                     │
│  eventos_vitais                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Controle de Acesso por Perfil

O sistema contará com três perfis de acesso para funcionários, cada um com permissões específicas por banco e operação:

| Operação / Dado                     | Recepcionista | Enfermeiro | Médico |
|------------------------------------|:-------------:|:----------:|:------:|
| Cadastro de pacientes (PG)          | ✅ Leitura/Escrita | ✅ Leitura | ✅ Leitura |
| Agendamentos (PG)                   | ✅ Leitura/Escrita | ✅ Leitura | ✅ Leitura/Escrita |
| Consultas clínicas (Mongo)          | ❌ | ✅ Leitura | ✅ Leitura/Escrita |
| Prescrições (Mongo)                 | ❌ | ✅ Leitura | ✅ Leitura/Escrita |
| Anamnese / Triagem (Mongo)          | ❌ | ✅ Leitura/Escrita | ✅ Leitura |
| Sinais vitais (Cassandra)           | ❌ | ✅ Leitura/Escrita | ✅ Leitura |
| Logs de acesso (Cassandra)          | ❌ | ❌ | ❌ (apenas admin) |
| Auditoria (Cassandra)               | ❌ | ❌ | ❌ (apenas admin) |
| Guias de atendimento (Mongo)        | ✅ Leitura | ✅ Leitura | ✅ Leitura/Escrita |

> **Nota:** Um perfil de `administrador` com acesso total será implementado separadamente para fins de manutenção e supervisão do sistema.

---

## 7. Requisitos Funcionais

### RF-01 — Gestão de Pacientes
- O sistema deve permitir cadastro, consulta, atualização e desativação de pacientes.
- Dados cadastrais devem ser armazenados no PostgreSQL com validação de CPF único.
- O histórico completo do paciente (consultas, exames, internações) deve ser acessível de forma consolidada.

### RF-02 — Gestão de Funcionários
- O sistema deve suportar o cadastro de recepcionistas, médicos e enfermeiros.
- Cada funcionário deve estar associado a um perfil de acesso que determina suas permissões.
- Médicos devem ter registro de CRM; enfermeiros, COREN.

### RF-03 — Agendamento de Consultas
- A recepcionista deve poder criar, editar e cancelar agendamentos.
- O sistema deve verificar conflitos de horário para o mesmo médico.
- Agendamentos devem ser armazenados no PostgreSQL.

### RF-04 — Registro de Consultas Médicas
- O médico deve poder registrar a transcrição da consulta, hipótese diagnóstica, CID-10 e prescrições.
- Os dados devem ser armazenados no MongoDB como um documento único e embarcado.
- Uma referência ao documento deve ser inserida na tabela `prontuario_ref` do PostgreSQL.

### RF-05 — Triagem e Anamnese
- O enfermeiro deve poder registrar a anamnese do paciente antes da consulta.
- Os dados de triagem (queixas, histórico familiar, alergias) devem ser armazenados no MongoDB.

### RF-06 — Monitoramento de Sinais Vitais
- Sinais vitais de pacientes internados devem ser registrados periodicamente pelo enfermeiro.
- Os dados devem ser gravados no Cassandra com timestamp e ordenados cronologicamente por internação.

### RF-07 — Logs e Auditoria
- Toda ação realizada no sistema (login, alteração de dados, acesso a prontuários) deve gerar um log no Cassandra.
- Alterações em dados críticos (pacientes, internações) devem registrar o valor anterior e o novo valor na tabela de auditoria.

### RF-08 — Fila de Atendimento
- O sistema deve registrar o histórico de estados da fila de atendimento por setor.
- Os dados devem ser armazenados no Cassandra para suportar alta volumetria.

---

## 8. Requisitos Não Funcionais

| ID     | Requisito                                                                                         |
|--------|---------------------------------------------------------------------------------------------------|
| RNF-01 | A camada de integração deve abstrair os três bancos, expondo uma API unificada (REST ou GraphQL)  |
| RNF-02 | Operações no PostgreSQL devem utilizar transações ACID para garantir integridade                  |
| RNF-03 | O MongoDB deve ser configurado com replica set para garantir durabilidade de documentos           |
| RNF-04 | O Cassandra deve ser configurado com fator de replicação ≥ 2 mesmo em ambiente de desenvolvimento |
| RNF-05 | A autenticação deve ser implementada com JWT, com claims indicando o perfil do funcionário        |
| RNF-06 | O projeto deve ser containerizado com Docker e orquestrado via Docker Compose               	     |
| RNF-07 | A documentação do schema de cada banco deve estar versionada no repositório                       |
| RNF-08 | O sistema deve incluir scripts de seed para popular os bancos com dados de teste                  |

---

## 9. Diagrama de Responsabilidades dos Bancos

```
                     REQUISIÇÃO DO USUÁRIO
                               │
                               ▼
                    ┌─────────────────────┐
                    │   API / Serviço     │
                    │   de Integração     │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
  ┌───────────────┐   ┌────────────────┐   ┌───────────────────┐
  │  PostgreSQL   │   │    MongoDB     │   │    Cassandra      │
  │               │   │                │   │                   │
  │ • Pacientes   │   │ • Consultas    │   │ • Logs de acesso  │
  │ • Funcionários│   │ • Anamneses    │   │ • Logs do sistema │
  │ • Agendamentos│   │ • Guias        │   │ • Auditoria       │
  │ • Referências │   │ • Resultados   │   │ • Filas           │
  │               │   │   de exames    │   │                   │
  │  ACID / CP    │   │  Flexível / AP │   │  Temporal / AP    │
  └───────────────┘   └────────────────┘   └───────────────────┘
```

---

## 10. Estrutura Sugerida do Repositório

```
databases/
│
├── README.md
├── docker-compose.yml              # Orquestração dos 3 bancos + API
│ 
├── postgres/
│   ├── schema.sql                  # DDL completo
│   ├── seeds.sql                   # Dados de teste
│   └── queries/                    # Consultas de exemplo
│
├── mongodb/
│   ├── schema/                     # JSON Schema para validação
│   ├── seeds/                      # Scripts de seed (.js ou .json)
│   └── queries/                    # Aggregation pipelines de exemplo
│
├── cassandra/
│   ├── schema.cql                  # Keyspace e tabelas
│   ├── seeds.cql                   # Dados iniciais
│   └── queries/                    # Consultas CQL de exemplo

api/
│
├── src/
│   ├── routes/
│   ├── services/
│   └── config/
└── .env.example
```

---

## 11. Tecnologias e Stack

| Categoria         | Tecnologia                    | Versão Sugerida |
|-------------------|-------------------------------|-----------------|
| Banco Relacional  | PostgreSQL                    | 16+             |
| Banco Documental  | MongoDB                       | 7+              |
| Banco Colunar     | Apache Cassandra              | 4.1+            |
| Containerização   | Docker + Docker Compose       | Latest          |
| API (opcional)    | Java + FastAPI  		    | Latest          |
| Driver Cassandra  | cassandra-driver (Python)     | Latest          |
| Autenticação      | JWT                           | —               |
| Documentação API  | Swagger / OpenAPI 3.0         | —               |

---

<div align="center">

---

*Documento elaborado para fins acadêmicos.*
*Sujeito a revisão conforme o andamento do projeto.*

</div>
