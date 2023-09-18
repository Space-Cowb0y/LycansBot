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

class TextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ()

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(923244743083819088)
        self.emojis = guild.emojis

    @commands.hybrid_command(name='decida', description="eu escolho pra você!",with_app_command=True)
    @app_commands.describe(escolhas="separar as opções por vírgula, tipo: 1,2,3,4")
    async def decida(self,ctx: Context,escolhas: str):
        sepa = escolhas.split(',')
        sepa = ''.join(sepa)
        sepa = sepa.split()
        if(len(sepa) < 2):
            await ctx.send('Cara, tu n\u00e3o me deu escolhas o suficiente',ephemeral=True)
        else:
            random.seed()
            choice = random.choices(sepa)
            if(choice[0] == ""):
                await ctx.send('Prefiro n\u00e3o escolher!',ephemeral=True)
            else:
                await ctx.send('Decidi ' + choice[0],ephemeral=True)
       
async def setup(bot):
    await bot.add_cog(TextCog(bot),guilds=[discord.Object(id=923244743083819088)])
    logger.info("Cog loaded: TextCog")