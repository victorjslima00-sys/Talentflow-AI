# Modelo de Ameaças & Checklist de Segurança

## 1. Modelo STRIDE Aplicado

| Ameaça (STRIDE) | Vetor Específico no TalentFlow AI | Contramedida de Engenharia |
|:---|:---|:---|
| **Spoofing (Falsificação)** | Atacante forja token de autenticação de outra empresa. | Assinatura JWT com chave secreta mínima de 32 bytes (`SecretStr`) e Argon2id para senhas. |
| **Tampering (Adulteração)** | Candidato submete arquivo executável disfarçado de PDF ou injeta prompt oculto. | Validação binária de `%PDF-` e sanitização rigorosa de texto com evidência literal obrigatória. |
| **Repudiation (Repúdio)** | Recrutador altera notas ou exclui candidatura sem registro. | Tabela `audit_log` imutável com data UTC, usuário e ação executada. |
| **Information Disclosure** | Empresa A acessa currículos ou vagas da Empresa B (BOLA). | `tenant_id` obrigatório em todas as queries e Row-Level Security no PostgreSQL. |
| **Denial of Service (DoS)** | Upload de arquivos gigantescos ou rajada de requisições de IA. | Limite de 5MB por arquivo, rate limiting via Redis e timeout estrito em workers. |
| **Elevation of Privilege** | Usuário comum tenta acessar painel de administração da plataforma. | Controle de acesso baseado em papéis (RBAC: Admin, Recruiter, Reviewer) verificado por dependências FastAPI. |

---

## 2. Checklist OWASP API Security Top 10

- [x] **API1:2023 - Broken Object Level Authorization (BOLA):** Mitigado com `tenant_id` e RLS.
- [x] **API2:2023 - Broken Authentication:** Mitigado com Argon2id, tokens de 15 min e cookies HttpOnly/Secure.
- [x] **API3:2023 - Broken Object Property Level Authorization:** Schemas Pydantic estritos para entrada e saída, impedindo mass assignment.
- [x] **API4:2023 - Unrestricted Resource Consumption:** Rate limiting e quotas por plano com atualização atômica no banco.
- [x] **API5:2023 - Broken Function Level Authorization:** Verificação de permissões em dependências declarativas nas rotas.
- [x] **API6:2023 - Unrestricted Access to Sensitive Business Flows:** Proteção contra raspagem de vagas públicas e submissões automatizadas em massa via rate limit e captcha.
- [x] **API7:2023 - Server-Side Request Forgery (SSRF):** Sem download arbitrário de URLs fornecidas por candidatos; uploads somente via multipart direto.
- [x] **API8:2023 - Security Misconfiguration:** Falha rápida na inicialização se faltar configuração ou se mock estiver ligado em produção.
- [x] **API9:2023 - Improper Inventory Management:** Documentação OpenAPI/Swagger versionada e schemas tipados.
- [x] **API10:2023 - Unsafe Consumption of APIs:** Tratamento de respostas de LLMs como dados não confiáveis com validação Pydantic.
