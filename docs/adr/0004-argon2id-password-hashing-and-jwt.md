# 4. Hashing de Senhas com Argon2id e Gerenciamento de Tokens com PyJWT

Data: 2026-10-29  
Status: Aceito

## Contexto
Bibliotecas legadas como `passlib` e `python-jose` encontram-se em estado de manutenção precário no ecossistema Python, apresentando alertas de compatibilidade com versões modernas do Python e do bcrypt.

## Decisão
Adotamos:
- **Argon2id** via `argon2-cffi`: Padrão recomendado pela OWASP para proteção contra ataques de força bruta acelerados por GPU/FPGA.
- **PyJWT**: Biblioteca ativa e robusta para assinatura e validação de tokens JWT.
- Tokens de acesso com vida curta (15 minutos).
- Refresh tokens rotativos armazenados com hash seguro no banco de dados e invalidação imediata em caso de logout ou detecção de reuso.
- Todos os campos de segredo no backend são envolvidos em `pydantic.SecretStr` e nunca são serializados ou expostos em logs.

## Consequências
- Máxima segurança criptográfica em repouso e em trânsito.
- Conformidade total com recomendações modernas da OWASP.
