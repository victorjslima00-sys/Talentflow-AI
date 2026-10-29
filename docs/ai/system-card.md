# Ficha do Sistema de IA (AI System Card) & Governança Ética

## 1. Descrição do Modelo e Uso Pretendido

- **Nome do Sistema:** TalentFlow Match Engine
- **Versão da Especificação:** 1.0.0
- **Finalidade:** Auxiliar recrutadores na classificação preliminar de compatibilidade entre o currículo do candidato e os requisitos declarados da vaga de emprego.
- **Uso Fora de Escopo:** O sistema **não** toma decisões autônomas de contratação, promoção ou demissão, e **não** realiza descarte automatizado de candidatos sem intervenção humana explícita.

---

## 2. Mitigação de Vieses & Teste Contrafactual de Paridade

### Medidas de Sanitização Prévia
Antes de enviar o conteúdo do currículo para o provedor de IA (`LLMProvider`):
1. **Redação de Identificadores Diretos:** Nomes, números de documentos (CPF), e-mails, telefones e endereços são removidos via regex e sanitizador especializado.
2. **Supressão de Atributos Protegidos:** Fotos, declarações explícitas de estado civil, gênero, idade ou religião não são repassadas ao prompt de análise.

### Teste Contrafactual no Pipeline de CI
Para assegurar a equidade do modelo:
- O pipeline de testes automatizados (`tests/test_bias_counterfactual.py`) avalia conjuntos sintéticos de currículos idênticos, alternando apenas marcas de gênero ou nomes socioculturais fictícios.
- **Critério de Aceite:** O `match_score` calculado para o mesmo histórico profissional deve permanecer dentro de uma margem de tolerância estatística estrita ($\le 3\%$).

---

## 3. Prevenção Contra Prompt Injection e Alucinações
- **Estruturação Rigorosa de Dados:** O currículo é passado como bloco delimitado de dados (JSON/XML tags fechadas).
- **Evidência Verificável:** Para cada competência ou lacuna apontada, a resposta da IA deve conter uma citação literal (`quote`) extraída diretamente do texto do currículo.
- O backend valida a existência exata do trecho citado; pontos sem evidência literal no texto original são sumariamente descartados pelo validador Pydantic.
