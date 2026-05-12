# PostgreSQL – Health Platform

Este container fornece um banco PostgreSQL para o projeto Health Platform.

Ele é usado principalmente para **dados relacionais e transacionais**, como:
- usuários
- profissionais de saúde
- unidades
- permissões
- dados normalizados



## 📦 Tecnologias
- PostgreSQL 16
- Docker / Docker Compose



## ▶️ Como subir o PostgreSQL isoladamente

A partir da pasta `postgres/`:

```bash
docker compose up -d
sudo docker exec -i health-postgres psql -U {user} -d {dbname} < postgresql/seeds/create_tables.sql 
