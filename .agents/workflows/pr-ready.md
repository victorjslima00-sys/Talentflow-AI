# /pr-ready Workflow

Procedimento de verificação executado antes de submeter qualquer Pull Request ao Tech Lead:

1. **Executar Linter e Formatador:**
   ```bash
   cd backend
   uv run ruff check .
   uv run ruff format --check .
   ```
2. **Executar Verificação Estrita de Tipos:**
   ```bash
   uv run mypy src tests
   ```
3. **Executar Suíte de Testes:**
   ```bash
   uv run pytest -v
   ```
4. **Executar Auditoria de Vulnerabilidades:**
   ```bash
   uv run pip-audit
   ```
5. **Varredura de Segredos:**
   ```bash
   gitleaks detect --no-git --verbose
   ```
6. **Compilar Relatório de Entrega:**
   - Resumo das mudanças
   - ADRs associados
   - Saída real dos comandos acima
   - Riscos identificados e mitigados
