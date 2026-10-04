import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from personality import SYSTEM_PROMPT

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_HISTORY = 10

historial = {}


class ChatIA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = None

        if API_KEY:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(
                    api_key=API_KEY,
                    base_url="https://api.groq.com/openai/v1"
                )
            except Exception as e:
                print(f"No se pudo inicializar el cliente de IA: {e}")
        else:
            print("GROQ_API_KEY no configurada. El chat IA estara desactivado.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user not in message.mentions:
            return

        if not self.client:
            await message.reply("El asistente de IA no esta configurado todavia.")
            return

        contenido = message.content
        for mention in message.mentions:
            contenido = contenido.replace(mention.mention, "").strip()

        if not contenido:
            await message.reply("Hola, soy AgroBot. Cuentame, ¿en que te puedo ayudar con tu cultivo?")
            return

        user_id = message.author.id
        historial.setdefault(user_id, []).append({"role": "user", "content": contenido})
        historial[user_id] = historial[user_id][-MAX_HISTORY:]

        async with message.channel.typing():
            try:
                respuesta = await self.client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial[user_id],
                    max_tokens=500,
                    temperature=0.7
                )
                texto = respuesta.choices[0].message.content
                historial[user_id].append({"role": "assistant", "content": texto})

                if len(texto) > 1900:
                    for i in range(0, len(texto), 1900):
                        await message.reply(texto[i:i + 1900])
                else:
                    await message.reply(texto)

            except Exception as e:
                print(f"Error IA: {e}")
                await message.reply("Uy, tuve un problema al procesar tu mensaje. Intenta de nuevo en un momento.")


async def setup(bot):
    await bot.add_cog(ChatIA(bot))