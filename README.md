# FarmOps Multi-Fazendas (FastAPI + PostgreSQL)

Sistema de gestão financeira e operacional de fazendas com **multi-tenant por fazenda** e **RBAC por módulo**.

## Stack
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- JWT access/refresh
- APScheduler
- Pytest
- Docker Compose

## Subir ambiente
1. Copie variáveis:
```bash
cp .env.example .env
```
2. Suba os serviços:
```bash
docker-compose up --build
```
3. Aplique views BI e seeds (opcional, após DB no ar):
```bash
docker-compose exec db psql -U postgres -d farmops -f /app/sql/views.sql
docker-compose exec db psql -U postgres -d farmops -f /app/seeds/seed_global_categories.sql
```

## Swagger
- `http://localhost:8000/docs`

## Multi-tenant
- Toda rota de domínio exige header `X-Farm-Id`.
- Membership é validado em dependências FastAPI.

## RBAC
- Papéis: OWNER, ADMIN, MANAGER, STAFF, VIEWER.
- Permissões em tabela `permissions` por módulo (read/write).
- Rotas exigem `require_permission(module, write=...)`.

## Migrações
```bash
alembic upgrade head
```

## Testes
```bash
pytest -q
```
