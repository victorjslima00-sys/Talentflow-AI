# 5. Fluxo de Autenticação com Cookies HttpOnly e Proteção CSRF

Data: 2026-10-29  
Status: Aceito

## Contexto
O armazenamento de tokens JWT em `localStorage` ou `sessionStorage` no navegador expõe os tokens a qualquer vulnerabilidade de Cross-Site Scripting (XSS), permitindo exfiltração silenciosa da sessão do usuário.

## Decisão
Os tokens de autenticação serão emitidos em cookies com as seguintes flags de segurança:
- `HttpOnly`: Impede acesso aos cookies via scripts JavaScript executados no cliente.
- `Secure`: Transmissão obrigatória via HTTPS (exceto em desenvolvimento local estritamente em `127.0.0.1`).
- `SameSite=Lax` ou `Strict`: Mitigação de requisições maliciosas entre origens distintas.
- Proteção adicional contra Cross-Site Request Forgery (CSRF) via cabeçalho customizado obrigatório (`X-Requested-With` ou token CSRF dedicado).

## Consequências
- Proteção robusta contra roubo de credenciais via XSS.
- Arquitetura limpa integrada entre Next.js Server Components e a API FastAPI.
