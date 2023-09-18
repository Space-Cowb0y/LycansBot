""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import platform
import random
import logging
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

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

class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="botinfo",description="Informações sobre essa bosta",with_app_command=True,)
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0x9C84EF,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="mitzrael.2170", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands para usar comandos normais",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="serverinfo",description="Obtenha informações importantes sobre o servidor.",with_app_command=True,)
    async def serverinfo(self, context: Context) -> None:
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Mostrando[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Nome do servidor:**", description=f"{context.guild}", color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="QTD Membros", value=context.guild.member_count)
        embed.add_field(
            name="Channels Texto/Voice", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Criado em: {context.guild.created_at}")
        await context.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="invite",description="Link de invite do bot =) (não usa vacilão)",with_app_command=True,)
    async def invite(self, context: Context) -> None:
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id=1151533949500260442&scope=bot+applications.commands&permissions=30781964545271&scope=bot%20applications.commands).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Te enviei lá no privado!")
        except discord.Forbidden:
            await context.send(embed=embed,ephemeral=True)

    @commands.hybrid_command(name="server",description="É o invite de um server ai...",with_app_command=True,)
    async def server(self, context: Context) -> None:
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here]().",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Te enviei lá no privado!")
        except discord.Forbidden:
            await context.send(embed=embed,ephemeral=True)

    @commands.hybrid_command(name="8ball",description="Pergunta que eu respondo.", with_app_command=True,)
    @app_commands.describe(pergunta="Fala a pergunta ai")
    async def eight_ball(self, context: Context, *, pergunta: str) -> None:
        answers = [
            "É certo.",
            "É decididamente assim.",
            "Você pode contar com isso.",
            "Sem dúvida.",
            "Sim - definitivamente.",
            "Como eu vejo, sim.",
            "Muito provável.",
            "Perspectiva boa.",
            "Sim.",
            "Sinais apontam para sim.",
            "Resposta vaga, tente novamente.",
            "Pergunte novamente mais tarde.",
            "Melhor não te dizer agora.",
            "Não é possível prever agora.",
            "Concentre-se e pergunte novamente mais tarde.",
            "Não conte com isso.",
            "Minha resposta é não.",
            "Minhas fontes dizem não.",
            "Perspectiva não tão boa.",
            "Muito duvidoso.",
        ]
        embed = discord.Embed(
            title="*Resposta:*",
            description=f"**{random.choice(answers)}**",
            color=0x9C84EF,
        )
        embed.set_footer(text=f"A Pergunta era: {pergunta}")
        await context.send(embed=embed,ephemeral=True)

    @commands.hybrid_command(name="bitcoin",description="Get the current price of bitcoin.",with_app_command=True,)
    async def bitcoin(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            ) as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript"
                    )  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF,
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed,ephemeral=True)


async def setup(bot):
    await bot.add_cog(General(bot))
    logger.info("Cog loaded: General")