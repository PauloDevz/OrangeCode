import os
import discord
from discord.ext import commands

# Import calculator functions
from calculadora import add, sub, mul, div

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='ping')
async def ping(ctx):
    """Responde com Pong!"""
    await ctx.send('Pong!')

@bot.command(name='calc')
async def calc(ctx, operation: str, a: float, b: float):
    """Executa uma operação básica usando o módulo calculadora.
    Uso: !calc <op> <a> <b>
    Operações suportadas: add, sub, mul, div
    """
    try:
        if operation == 'add':
            result = add(a, b)
        elif operation == 'sub':
            result = sub(a, b)
        elif operation == 'mul':
            result = mul(a, b)
        elif operation == 'div':
            result = div(a, b)
        else:
            await ctx.send('Operação desconhecida. Use add, sub, mul ou div.')
            return
        await ctx.send(f'Resultado: {result}')
    except ZeroDivisionError as e:
        await ctx.send(str(e))
    except Exception as e:
        await ctx.send(f'Erro ao calcular: {e}')

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise RuntimeError('Variável de ambiente DISCORD_TOKEN não definida.')
    bot.run(token)
