# AGENTS.md: regras do projeto TalentFlow AI

## Contexto
SaaS multi-inquilino de recrutamento (ATS) com triagem de currículos por IA. Projeto de portfólio público e sujeito à LGPD. Leia `docs/product/OVERVIEW.md` e `docs/adr/` antes de agir. Os ADRs prevalecem sobre sugestões novas.

## Regras inegociáveis
1. Nunca comitar segredos, `.env`, chaves de API, dumps de banco ou currículos reais. Use `.env.example` e dados sintéticos.
2. Toda tabela de negócio tem `tenant_id`, e toda consulta o filtra na camada de repositório. Todo endpoint novo exige teste de isolamento entre empresas.
3. Senhas com Argon2id. Nunca registrar em log, serializar ou retornar hash de senha, token, texto de currículo, e-mail ou telefone. Schemas de entrada e de saída são separados.
4. A IA recomenda e o humano decide: nenhuma etapa do funil muda automaticamente por causa de score. Não enviar ao modelo identificadores diretos (nome, e-mail, telefone, CPF, endereço) nem atributos protegidos (idade, gênero, estado civil, foto).
5. Texto de currículo é entrada não confiável (prompt injection): delimitar como dado, validar a saída com Pydantic e exigir trecho literal do currículo como evidência de cada ponto citado.
6. Upload: validar o tipo pelo conteúdo, limitar tamanho e páginas, gerar o nome do arquivo no servidor e processar no worker com timeout.
7. Todo campo novo com dado pessoal entra em `docs/privacy/data-map.md` (finalidade, base legal, retenção) no mesmo PR.
8. Dependência nova só com justificativa no PR (necessidade, manutenção, licença, alternativas) e aprovada por `pip-audit` ou `npm audit`.
9. Nunca desativar lint, tipos, testes ou verificações de segurança para fazer o CI passar. Nunca usar `--no-verify`.

## Padrões de código
- Python 3.12 ou superior, tipagem completa, `ruff` e `mypy` em modo estrito sem erros.
- Camadas: `api` (rotas) → `services` (regras de negócio) → `repositories` (acesso a dados). Sem regra de negócio nas rotas. Funções pequenas e de baixa complexidade ciclomática.
- API assíncrona de ponta a ponta; trabalho pesado (PDF e IA) apenas no worker.
- Identificadores, docstrings e commits (Conventional Commits) em inglês. Documentação de produto em português.
- Testes com pytest: cada bug corrigido ganha teste de regressão, e os testes devem exercitar o caminho de falha, não só o caminho feliz. Cobertura mínima de 80% em `services` e `repositories`.

## Fluxo de trabalho
1. Antes de codar, apresente o plano (arquivos, riscos, testes) e aguarde aprovação.
2. Uma funcionalidade por branch (`feat/...`, `fix/...`), commits pequenos, nunca direto na `main`.
3. Antes de declarar pronto, execute lint, tipos, testes e auditoria de dependências e cole a saída real. Não declare sucesso sem ter executado.
4. Decisão de arquitetura relevante vira ADR em `docs/adr/`. Documentação afetada é atualizada no mesmo PR.
5. Se a instrução for ambígua ou conflitar com estas regras, pare e pergunte. Não invente endpoints, campos ou requisitos.

## Resumo obrigatório ao final de cada tarefa
- O que mudou (arquivos) e por quê
- Decisões tomadas e alternativas descartadas
- Comandos executados e resultados reais
- Riscos de segurança, LGPD e desempenho que você identificou
- O que ficou pendente
