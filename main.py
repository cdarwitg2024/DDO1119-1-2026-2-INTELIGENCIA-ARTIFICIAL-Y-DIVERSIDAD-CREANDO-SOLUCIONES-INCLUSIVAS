import os
import asyncio
import threading
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask('')

@app.route('/')
def home():
    return "Salphine 🌱 está despierta y cuidando el campo."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web_server)
    t.start()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("========================================")
    print("Bot conectado con éxito a Discord")
    print(f"Nombre del Bot: {bot.user.name}")
    print(f"ID del Bot: {bot.user.id}")

    try:
        synced = await bot.tree.sync()
        print(f"Se han sincronizado {len(synced)} comandos Slash.")
    except Exception as e:
        print(f"Error al sincronizar comandos Slash: {e}")

    print("========================================")

async def load_extensions():
    if not os.path.exists("cogs"):
        os.makedirs("cogs")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"Módulo cargado: {cog_name}")
            except Exception as e:
                print(f"Error al cargar {cog_name}: {e}")

async def main():
    keep_alive()
    async with bot:
        await load_extensions()
        if not TOKEN or TOKEN == "TU_TOKEN_AQUI":
            print("ERROR: Configura tu DISCORD_TOKEN en el archivo .env o variables de entorno")
            return
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot apagado manualmente.")