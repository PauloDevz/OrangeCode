# Discord Bot

Este é um bot simples para Discord escrito em Python usando a biblioteca **discord.py**.

## Funcionalidades
- `!ping` – Responde com *Pong!* para testar se o bot está online.
- `!calc <op> <a> <b>` – Executa operações básicas de cálculo usando o módulo **calculadora** já presente no projeto.
  - Operações suportadas: `add`, `sub`, `mul`, `div`.

## Requisitos
- Python 3.8 ou superior
- Biblioteca `discord.py` (instalada via `pip install -r requirements.txt`)

## Configuração
1. Crie um bot no portal do Discord e obtenha o token.
2. Defina a variável de ambiente `DISCORD_TOKEN` com o token do seu bot:
   ```bash
   export DISCORD_TOKEN='seu_token_aqui'
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução
```bash
python discord_bot.py
```

O bot se conectará ao Discord e ficará pronto para responder aos comandos acima.
