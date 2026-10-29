# 3. Abstração de Provedor de IA com SDK Direto (sem LangChain)

Data: 2026-10-29  
Status: Aceito

## Contexto
Estruturas pesadas de orquestração como o LangChain introduzem árvores extensas de dependências, quebras frequentes de compatibilidade entre versões secundárias e camadas desnecessárias de abstração para chamadas com esquemas JSON estruturados.

## Decisão
Utilizaremos chamadas diretas de SDK organizadas atrás de uma interface abstrata `LLMProvider`:
- `MockProvider`: Fornece respostas determinísticas e sintéticas para testes locais e CI sem custos de API.
- `GeminiProvider`: Integração direta via SDK oficial do Google Gemini com saída estruturada Pydantic.
- `OpenAIProvider`: Integração direta via cliente OpenAI com `response_format`.

A inicialização da aplicação deve validar estritamente o ambiente: se `APP_ENV=production` e `LLM_PROVIDER=mock`, a aplicação falhará imediatamente na inicialização para impedir acidentes.

## Consequências
- Código limpo, testável e transparente.
- Zero dependências instáveis ou transitivas desnecessárias.
- Possibilidade de alternar provedores sem alterar o código de serviço de domínio.
