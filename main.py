import os
import discord
from discord import app_commands
from config import get_settings
from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Message, Guild

from dotenv import load_dotenv

load_dotenv()

DEBUG = get_settings().DEBUG

BOT_TOKEN = get_settings().BOT_TOKEN

class MyClient(commands.Bot):
    async def on_ready(self):
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
            for command in synced:
                print(f"Command: {command}")
        except Exception as e:
            print(e)
            exit()
        print("------")
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        for guild in self.guilds:
            print(f"--- {guild.name} ---")
            for member in guild.members:
                print(member)
            print(f"--- end ---\n\n")
        print("--- Ready ---")

    async def setup_hook(self):
        for extension in cogs:
            await self.load_extension(extension)

    async def on_guild_join(self, guild: Guild):
        for channel in guild.text_channels:
            print(channel.name)
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f"Olá, {guild.name}, eu sou Jotchua!")
            break

    async def on_message(self, message: Message):
        await self.process_commands(message)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
command_prefix = ["jot!", "j!"]

cogs = ["src.comandos.basic", "src.comandos.social"]

client = MyClient(intents=intents, command_prefix=command_prefix)
client.run(BOT_TOKEN)
