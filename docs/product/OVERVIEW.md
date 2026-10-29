# Visão Geral do Produto — TalentFlow AI

## 1. O Problema
Recrutadores gastam mais de 70% do tempo inicial do processo seletivo lendo currículos de forma manual, repetitiva e suscetível a cansaço e vieses inconscientes. Candidatos qualificados são frequentemente perdidos em caixas de entrada desorganizadas, enquanto a empresa sofre com alto *Time-to-Hire* (tempo até a contratação).

## 2. A Solução
O **TalentFlow AI** é uma plataforma ATS moderna que automatiza a triagem de currículos utilizando Inteligência Artificial explicável, ética e aderente à LGPD.

### Funcionalidades Centrais:
1. **Estruturação Inteligente de Vagas:** Transforma descrições brutas e informais em requisitos estruturados (título, senioridade, requisitos mandatórios com pesos, diferenciais e palavras-chave).
2. **Página Pública de Inscrição:** Canal seguro e responsivo para candidatos enviarem dados e submeterem currículos em formato PDF.
3. **Engine de Extração e Aderência:**
   - Extrai texto do PDF com validação rigorosa de assinatura binária `%PDF-`.
   - Realiza sanitização prévia removendo dados pessoais identificáveis (nome, CPF, telefone, e-mail) antes de submeter ao modelo de linguagem.
   - Calcula o Match Score (0 a 100%) baseado em **evidências literais** citadas do currículo, eliminando alucinações e prompt injections.
4. **Funil de Candidatos (Pipeline Kanban):**
   - Transições de etapa transparentes: *Inscrito ➔ Triagem IA ➔ Análise Humana ➔ Entrevista ➔ Proposta ➔ Aprovado / Reprovado*.
   - **Regra Fundamental de IA:** A IA apenas recomenda e pontua; a transição para etapas decisivas e reprovação é exclusivamente humana.
5. **Portal do Titular (LGPD Art. 18):**
   - Link de acesso exclusivo enviado ao candidato para consulta, retificação e solicitação de eliminação definitiva com anonimização.
