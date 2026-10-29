# Registro de Revisão #000 — Kickoff e Aprovação do Plano da Fase 0

Data: 2026-10-29  
Revisor: Tech Lead  
Implementador: Antigravity  
Status: Aprovado

---

## 1. Veredito
**Aprovado**. O plano de implementação da Fase 0 atende a todas as restrições inegociáveis de governança, isolamento de inquilinos, conformidade com a LGPD e testes prévios de portão de qualidade.

---

## 2. Decisões Confirmadas
- Fila assíncrona: Celery + Redis com idempotência.
- IA: SDK direto sob a interface `LLMProvider` (sem LangChain).
- Senhas e Tokens: Argon2id (`argon2-cffi`) e `PyJWT`.
- Tokens Web: Cookies `HttpOnly`, `Secure` e `SameSite`.
- PDF: `pypdf` com validação binária de assinatura `%PDF-`.
- Idioma: Código e commits em inglês; documentação de produto em português.
- Licença: MIT.
- Visibilidade: Repositório privado inicial com abertura pública após varredura do histórico pelo `gitleaks`.

---

## 3. O Que Você Precisa Entender (Para Entrevistas Técnicas)
- **Por que `tenant_id` em todas as tabelas e não só na vaga?**  
  Em APIs REST complexas, a falta de `tenant_id` direto na tabela de candidaturas ou avaliações força o sistema a fazer joins sucessivos para checar permissão. Um único esquecimento em uma query pode abrir uma falha BOLA (Broken Object Level Authorization), expondo currículos de uma empresa para outra. O `tenant_id` em cada tabela permite checagem imediata, índices compostos de alta performance e viabiliza o Row-Level Security nativo do PostgreSQL.
- **Por que não rodar IA e PDFs no loop do FastAPI nem em `BackgroundTasks`?**  
  `BackgroundTasks` do FastAPI roda na mesma memória do processo da API. Se o container reiniciar ou receber um SIGTERM durante o processamento de um currículo, a tarefa é perdida para sempre sem reprocessamento. Além disso, parsing de PDF consome CPU, podendo bloquear o loop assíncrono do FastAPI e degradar o tempo de resposta de outros usuários. Celery + Redis garante filas duráveis, retentativas automáticas e escalabilidade horizontal independente.
