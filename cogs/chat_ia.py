import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from personality import SYSTEM_PROMPT

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
MAX_HISTORY = 10

historial = {}


class ChatIA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = None

        if GROQ_API_KEY:
            try:
                from groq import AsyncGroq
                self.client = AsyncGroq(api_key=GROQ_API_KEY)
            except Exception as e:
                print(f"No se pudo inicializar el cliente de Groq: {e}")
        else:
            print("GROQ_API_KEY no configurada. El chat de texto estara desactivado.")

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
                    model=GROQ_MODEL,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historial[user_id],
                    max_tokens=500,
                    temperature=0.7
                )
                texto = respuesta.choices[0].message.content

                if texto:
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