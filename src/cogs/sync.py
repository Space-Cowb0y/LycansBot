import logging
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import random


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

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ()
    
    @commands.command(name='sync',description='sincroniza os comandos co o discord',with_app_command=True,)
    @commands.guild_only()
    async def sync(self,ctx) -> None:
            synced = await ctx.bot.tree.sync()
            await ctx.send(f"{len(synced)} comandos sincronizados",ephemeral=True)
            return
        
async def setup(bot):
    await bot.add_cog(Sync(bot),guilds=[discord.Object(id=923244743083819088)])
    logger.info("Cog loaded: Sync")