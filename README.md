
---

## 🗄️ Health Databases – Infraestrutura de Dados

```md
# Health Databases – Infraestrutura de Dados

Este repositório centraliza os containers de bancos de dados utilizados no projeto Health Platform.

Ele existe para facilitar:
- o desenvolvimento local
- a padronização do ambiente
- a inicialização rápida de todos os bancos necessários

Os bancos aqui definidos são consumidos pelo backend da aplicação.

---

## 📦 Tecnologias
- PostgreSQL
- MongoDB
- Apache Cassandra
- Docker / Docker Compose

---

## ▶️ Como subir todos os bancos

A partir da raiz do repositório:

```bash
docker compose up -d
