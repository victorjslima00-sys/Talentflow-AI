# 6. Estratégia de Upload, Validação e Extração de Currículos em PDF

Data: 2026-10-29  
Status: Aceito

## Contexto
O upload de arquivos é um vetor crítico de ataque (upload de binários maliciosos, zip bombs, ataques de negação de serviço e injeção de instruções).

## Decisão
1. **Validação Mágica de Conteúdo:** O backend valida os primeiros bytes do arquivo garantindo a assinatura binária `%PDF-` (`0x25 0x50 0x44 0x46 0x2D`), rejeitando arquivos baseados unicamente na extensão `.pdf`.
2. **Limites Rígidos:** Tamanho máximo de 5MB e limite de até 5 páginas por currículo.
3. **Armazenamento Seguro:** Arquivos recebem identificadores UUID gerados no servidor, são salvos fora de diretórios públicos acessíveis pela web e são servidos exclusivamente por URLs assinadas de curta duração.
4. **Extração de Texto:** Executada assincronamente com `pypdf`. Se o documento não contiver texto extraível (ex: PDF escaneado puramente como imagem), o sistema retorna um erro amigável ao candidato solicitando um PDF com texto selecionável (OCR está fora do escopo).
5. **Mitigação de Prompt Injection:** O texto extraído é tratado estritamente como dado não confiável. O prompt delimita blocos de texto e a saída é obrigada a conter evidências literais existentes no texto original.

## Consequências
- Alta segurança contra ataques de infraestrutura.
- Proteção contra alucinações e prompt injection por candidatos maliciosos.
