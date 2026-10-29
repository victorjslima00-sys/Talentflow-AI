# 7. Isolamento Multi-inquilino (Multi-Tenancy) e Row-Level Security (RLS)

Data: 2026-10-29  
Status: Aceito

## Contexto
O vazamento de dados entre empresas clientes (Broken Object Level Authorization - BOLA) é uma das vulnerabilidades mais graves em sistemas SaaS multi-inquilinos. Confiar exclusivamente no middleware da aplicação é arriscado caso um desenvolvedor esqueça uma cláusula `WHERE` em uma nova consulta.

## Decisão
Implementamos defesa em profundidade em duas camadas:
1. **Camada de Aplicação/Repositório:** Toda tabela de domínio possui coluna `tenant_id NOT NULL REFERENCES tenants(id)`. Todos os métodos de consulta nos repositórios exigem o parâmetro `tenant_id` e filtram explicitamente por ele.
2. **Camada de Banco de Dados (Row-Level Security):** O PostgreSQL RLS será ativado em todas as tabelas de negócio, associando a sessão da conexão ao tenant ativo (`SET LOCAL app.current_tenant_id = '...'`).
3. **Testes de Isolamento Obrigatórios:** Cada novo endpoint de leitura, escrita ou exclusão deve ter um teste automatizado demonstrando que um usuário autenticado da Empresa A recebe `404 Not Found` ou `403 Forbidden` ao tentar interagir com recursos da Empresa B.

## Consequências
- Garantia matemática e estrutural de segregação de dados.
- Impossibilidade de vazamento acidental entre clientes.
