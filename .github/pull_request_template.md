## 📌 Descrição da Mudança
<!-- Descreva de forma clara e concisa o que foi implementado ou corrigido e a motivação. -->

## 🎯 Tipo de Mudança
- [ ] Nova funcionalidade (`feat`)
- [ ] Correção de bug (`fix`)
- [ ] Refatoração ou melhoria de performance (`refactor` / `perf`)
- [ ] Documentação ou ADR (`docs`)
- [ ] Infraestrutura, CI/CD ou dependências (`ci` / `chore`)

## 🛡️ Checklist de Qualidade e Governança (Obrigatório)
- [ ] **Zero Segredos:** Nenhuma chave, senha, `.env` ou dado confidencial incluído (validado com `gitleaks`).
- [ ] **Isolamento de Tenants:** Toda tabela tocada possui `tenant_id` e há teste garantindo que a Empresa A não acessa dados da Empresa B.
- [ ] **LGPD / Privacidade:** Se novos campos de dados pessoais foram adicionados, foram registrados em `docs/privacy/data-map.md`.
- [ ] **IA Ética & Prompt Injection:** Entradas de currículo são tratadas como dados não confiáveis com evidência verificável; decisões de reprovação nunca são automáticas.
- [ ] **Testes Automatizados:** Testes reais adicionados cobrindo casos de sucesso e caminhos de falha (cobertura >= 80% em services/repositories).
- [ ] **Portão Local Aprovado:**
  - `uv run ruff check .` sem erros
  - `uv run ruff format --check .` sem erros
  - `uv run mypy src tests` em modo estrito sem erros
  - `uv run pytest -v` todos passando
  - `uv run pip-audit` sem vulnerabilidades conhecidas

## 📋 ADRs e Documentação
<!-- Cite os ADRs criados ou atualizados relacionados a este PR -->
- [ ] ADR atualizado/criado em `docs/adr/` (se aplicável)
