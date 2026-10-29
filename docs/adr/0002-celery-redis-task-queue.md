# 2. Utilização de Celery e Redis para Filas Assíncronas

Data: 2026-10-29  
Status: Aceito

## Contexto
O processamento de currículos envolve extração de texto de PDFs e requisições HTTP para modelos de IA, que podem levar de 2 a 15 segundos. Executar essas operações no loop de eventos principal da API (FastAPI) ou via `BackgroundTasks` em memória é arriscado, pois tarefas em memória são perdidas em caso de reinicialização do processo e não oferecem controle robusto de concorrência ou retentativas.

## Decisão
Adotamos **Celery com Redis** como backend de mensageria e armazenamento de resultados. Todas as tarefas de parsing de PDF, higienização de PII e avaliação de IA serão despachadas para filas dedicadas do Celery com:
- Tarefas idempotentes (baseadas em chave de unicidade de candidatura).
- Política de retry com backoff exponencial.
- Separação de prioridades de fila (ex: processamento urgente vs. reanálise em lote).

## Consequências
- A API responde à submissão do currículo em menos de 100ms (`202 Accepted`).
- Resiliência total contra falhas transientes de rede ou de provedores de IA.
