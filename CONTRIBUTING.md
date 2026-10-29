# Guia de Contribuição (Contributing Guide)

Obrigado pelo interesse em contribuir com o **TalentFlow AI**! Para manter a excelência técnica, segurança e conformidade com a LGPD, seguimos regras estritas de desenvolvimento.

---

## 1. Fluxo de Trabalho e Branches

- Toda alteração deve ser desenvolvida em uma branch separada:
  - Novas funcionalidades: `feat/nome-da-feature`
  - Correção de bugs: `fix/nome-do-bug`
  - Documentação: `docs/nome-da-melhoria`
- **Nunca comite diretamente na branch `main`.**
- O histórico de commits segue rigorosamente a convenção [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat: add candidate application endpoint with rls`
  - `fix: prevent potential path traversal on pdf upload`
  - `test: add tenant isolation regression test for jobs api`
  - `docs: update adr-0004 with argon2id parameters`

---

## 2. Portão de Qualidade Obrigatório (Definition of Done)

Antes de abrir um Pull Request, certifique-se de que todos os comandos locais passam sem nenhum aviso ou erro:

```bash
# No diretório backend/
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest -v
uv run pip-audit
```

Além disso, verifique a ausência de credenciais ou dados pessoais:
```bash
gitleaks detect --no-git --verbose
```

---

## 3. Regras Inegociáveis
1. **Zero Segredos:** Nunca inclua chaves de API, senhas ou arquivos `.env`.
2. **Isolamento de Tenants:** Qualquer novo endpoint deve conter testes comprovando que a Empresa A não acessa, edita ou exclui dados da Empresa B.
3. **Privacidade (LGPD):** Campos com dados pessoais devem ser mapeados em `docs/privacy/data-map.md`.
4. **Decisões Registradas:** Mudanças arquiteturais requerem um novo Architecture Decision Record (ADR) em `docs/adr/`.
