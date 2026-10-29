# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Added
- **Fase 0: Fundação do Repositório & Governança**
  - Estrutura base de pastas (`backend/`, `frontend/`, `docs/`, `.github/`, `.agents/`).
  - Arquivo `AGENTS.md` com diretrizes inegociáveis de segurança, LGPD e limites de automação para agentes.
  - Configuração do `docker-compose.yml` para PostgreSQL 16 e Redis 7 com binding restrito a `127.0.0.1`.
  - Configuração de linter e formatação com `ruff` e tipagem estrita com `mypy`.
  - Endpoint mínimo `GET /health` com validação de schema e teste automatizado via `pytest`.
  - Pipeline de CI no GitHub Actions com lint, types, tests, pip-audit e gitleaks.
  - Documentação inicial com ADRs 0001 a 0008, Modelo de Ameaças, Mapa de Dados LGPD e AI Workflow.
