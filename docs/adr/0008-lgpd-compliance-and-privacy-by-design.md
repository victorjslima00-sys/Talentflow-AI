# 8. Conformidade com a LGPD e Privacy by Design

Data: 2026-10-29  
Status: Aceito

## Contexto
Currículos contêm dados pessoais (nome, e-mail, telefone, histórico profissional) e frequentemente dados sensíveis (fotos, filiação, deficiências). A LGPD (Lei 13.709/2018) impõe deveres claros para controladores e operadores, garantindo direitos aos titulares (Art. 18 e Art. 20).

## Decisão
1. **Definição Clara de Papéis:**
   - Dados de candidatos a vagas: A empresa cliente é **Controladora**; o TalentFlow AI atua como **Operador**.
   - Dados de recrutadores e faturamento: O TalentFlow AI é **Controlador**.
2. **Modelo de Dados Segregado:**
   - Separação entre `Candidate` (dados cadastrais do titular) e `Application` (candidatura vinculada a uma vaga).
   - Coluna `extracted_resume_text` possui acesso altamente restrito e ciclo de retenção temporário curto.
3. **Direitos do Titular (Art. 18):**
   - Disponibilização do **Portal do Titular** acessível por link com token seguro enviado ao e-mail do candidato.
   - Suporte a eliminação real e irreversível (com anonimização de métricas históricas) e exportação de dados em formato legível por máquina (JSON).
4. **Decisão Automatizada e Não Discriminação (Art. 20):**
   - A IA calcula pontuação e elenca evidências, mas **reprovações e avanços de fase são sempre deliberados por humanos**.
   - Currículos enviados a provedores de IA são previamente anonimizados (remoção de dados de contato e atributos protegidos).
   - Teste contrafactual de viés executado no CI com currículos sintéticos variando atributos protegidos para auditar paridade estatística do modelo.

## Consequências
- Postura de privacidade transparente, ética e diferenciada para portfólio.
- Redução drástica de risco de responsabilidade civil ou multas da ANPD.
