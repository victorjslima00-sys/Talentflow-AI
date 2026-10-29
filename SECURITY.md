# Política de Segurança (Security Policy)

## Relato de Vulnerabilidades

A segurança do **TalentFlow AI** e a privacidade dos dados de candidatos e empresas são prioridades absolutas. Se você descobrir uma vulnerabilidade de segurança, agradecemos a sua comunicação responsável.

**Por favor, não abra issues públicas no GitHub para relatar vulnerabilidades de segurança.**

### Como reportar:
Envie um e-mail com os detalhes técnicos da vulnerabilidade para:
- **Contato de Segurança:** `security@talentflow.local` (ou abra um *Security Advisory* privado no repositório GitHub)

### O que incluir no seu relatório:
1. Descrição clara da vulnerabilidade e seu potencial impacto.
2. Passos reproduzíveis (PoC ou script/requisições HTTP necessárias).
3. Componentes afetados (ex: endpoint da API, middleware de tenant, parser de PDF).
4. Sugestão de correção, caso possua.

Responderemos em até 48 horas úteis com a confirmação de recebimento e um plano de ação para contenção e correção.

---

## Diretrizes de Segurança do Projeto
- **Isolamento de Tenants:** Toda tabela de negócio possui `tenant_id` e filtragem obrigatória na camada de repositório e via RLS.
- **Proteção de Segredos:** O repositório utiliza verificação contínua via `gitleaks` para garantir que nenhuma chave ou dado confidencial seja comitado.
- **LGPD & Privacidade:** Nenhum dado pessoal identificável ou sensível é enviado a modelos de IA de terceiros sem sanitização prévia.
- **Defesa contra Prompt Injection:** Currículos são tratados estritamente como dados não confiáveis, exigindo validação estruturada com Pydantic e evidência verificável de trechos literais.
