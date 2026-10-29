# Mapeamento de Dados Pessoais & Governança LGPD (Data Map)

## 1. Inventário de Dados Pessoais

| Dado Pessoal | Categoria | Titular | Finalidade do Tratamento | Base Legal (Art. 7º LGPD) | Retenção Prevista | Medida de Segurança |
|:---|:---|:---|:---|:---|:---|:---|
| **Nome Completo** | Pessoal comum | Candidato | Identificação no processo seletivo | Consentimento / Execução de contrato | N dias após encerramento da vaga | Acesso restrito a recrutadores |
| **E-mail & Telefone** | Contato | Candidato | Comunicação de etapas e convocação | Consentimento / Execução de contrato | N dias após encerramento da vaga | Mascarado antes do envio à IA |
| **Currículo (PDF)** | Profissional | Candidato | Avaliação de competências para a vaga | Consentimento / Legítimo interesse | Retenção máxima de 1 ano | Armazenamento privado fora do webroot |
| **Texto Extraído** | Profissional | Candidato | Extração de skills e análise de match | Consentimento / Legítimo interesse | Retenção de 30 dias (temporário) | Acesso técnico exclusivo do worker |
| **Score & Parecer IA** | Gerado/Derivado | Candidato | Apoio à decisão de triagem do recrutador | Legítimo interesse do controlador | Histórico da vaga | Auditável com justificativa literal |
| **E-mail do Recrutador**| Corporativo | Recrutador | Autenticação e gestão de conta SaaS | Execução de contrato SaaS | Duração do contrato da empresa | Hash Argon2id para senhas |

---

## 2. Direitos do Titular (Art. 18 LGPD)

1. **Confirmação e Acesso:** Candidato recebe link único (*magic link*) ao se inscrever para visualizar seus dados armazenados.
2. **Correção:** Possibilidade de atualizar dados cadastrais antes do encerramento da triagem da vaga.
3. **Eliminação Real / Anonimização:** Ao solicitar exclusão pelo Portal do Titular:
   - Os arquivos PDF são permanentemente deletados do storage.
   - Os dados identificáveis são anonimizados (substituídos por hashes irreversíveis), preservando apenas estatísticas agregadas da vaga.
   - O evento de exclusão é registrado na tabela de auditoria com timestamp UTC.
