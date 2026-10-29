# Arquitetura e Fronteiras de Componentes

## 1. Visão Geral dos Módulos

```mermaid
flowchart TD
    subgraph Edge ["Borda e Segurança"]
        Nginx["Reverse Proxy / TLS Termination"]
        RateLimiter["Rate Limiter (Redis)"]
    end

    subgraph API ["Backend API (FastAPI)"]
        HealthRouter["/health"]
        AuthRouter["/api/v1/auth (Argon2id + JWT HttpOnly)"]
        JobRouter["/api/v1/jobs (CRUD + Structuring)"]
        CandidateRouter["/api/v1/candidates (Upload & Candidatura)"]
        SubjectPortalRouter["/api/v1/privacy/subject-portal (Art. 18 LGPD)"]
    end

    subgraph AsyncWorker ["Workers Assíncronos (Celery)"]
        ResumeParser["PDF Signature Validator & Text Extractor"]
        PIISanitizer["PII Masker / Redactor"]
        AIAnalyzer["LLM Analyzer (Interface LLMProvider)"]
    end

    subgraph Persistence ["Persistência de Dados"]
        Postgres[(PostgreSQL 16 com RLS)]
        RedisCache[(Redis 7)]
    end

    Edge --> API
    API --> Postgres
    API --> RedisCache
    API --> AsyncWorker
    AsyncWorker --> Postgres
```

## 2. Princípios de Isolamento
- **Multi-Tenancy:** Todas as tabelas têm coluna `tenant_id`.
- **Filtro em Camadas:** Repositórios filtram obrigatoriamente por `tenant_id`. PostgreSQL Row-Level Security (RLS) atua como segunda linha de defesa em profundidade.
- **Isolamento de Tarefas:** Workers recebem o identificador da candidatura e resolvem o tenant no contexto de execução, garantindo que logs e métricas permaneçam segregados.
