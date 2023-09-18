import gettext
import json
import logging
import os
import asyncio
from datetime import datetime
import traceback
import logging
import sys
import copy
import json
import sqlite3
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

# no logs no crime
logfile = "bot.log"
logging.basicConfig(
    filename=logfile,
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.logger = logger

#carrega env e token
load_dotenv()
try:
    token = os.getenv("token")
except KeyError:
    logging.critical("Please supply a discord bot token.")
    raise SystemExit

intents = discord.Intents.all()
intents.members = True
intents.message_content = True


#configurações do bot 
bot = commands.Bot(command_prefix='/',
                   case_insensitive=True,
                   intents=intents,
                   activity=discord.Game(name="com a API do discord"),
                   )

# verifica se pode receber dms
def globally_block_dms(bot):
    if bot.guild is None:
        raise commands.NoPrivateMessage("No dm allowed!")
    else:
        return True

bot.add_check(globally_block_dms)

#verifica se está em uma guild  
@bot.event
async def on_ready(): 
    logger.info('------')    
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    if not bot.guilds:
        logger.error("The bot is not in any guilds. Shutting down.")
        await bot.close()
        return
    for guild in bot.guilds:
            logger.info("Welcome to {0}.".format(guild))
            logger.info('------')
            
async def on_command_error(error):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send(_("Please use this command in a server."))
    else:
        if not isinstance(error, commands.CommandNotFound):
            logger.warning("Error for command: " + bot.message.content)
            logger.warning(error)
        try:
            await bot.send(error, delete_after=10)
        except discord.Forbidden:
            logger.warning(
                "Missing Send messages permission for channel {0}".format(
                    bot.channel.id
                )
            )

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())

logger.info("Shutting down.")