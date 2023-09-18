import platform
import datetime
import random
import logging
from typing import List
import aiohttp
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context

emojis = {
    "dps": "<:dps:1151585351631114290>",
    "support": "<:support:1151585350347657420>",
    "healer": "<:healer:1151588279985119282>",
    "tanker": "<:tanker:1151585347399073832>",
    "Lista de Espera": "<:try:1151585352780353588>",
}

emoji_to_field = {
    emojis["dps"]: f'{emojis["dps"]} DPS',
    emojis["support"]:f'{emojis["support"]} Support',
    emojis["healer"]: f'{emojis["healer"]} Healer',
    emojis["tanker"]: f'{emojis["tanker"]} Tank',
    emojis["Lista de Espera"]: f'{emojis["Lista de Espera"]} Lista de Espera',
}

limites = {
    "Fractal": {
            "DPS": 2,
            "Support": 2,
            "Healer": 1,
            "Lista de Espera": 50,
        },
    "Strike": {
            "DPS": 4,
            "Support": 4,
            "Healer": 2,
            "Lista de Espera": 50,
        },
    "Raid": {
            "DPS": 4,
            "Support": 4,
            "Healer": 2,
            "Tank": 1,
            "Lista de Espera": 50,
        },
    "Meta": {
            "DPS": 50,
            "Support": 50,
            "Healer": 50,
            "Tank": 50,
            "Lista de Espera": 50,
        },
}

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

class Evento(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ()
        self.usuarios_reagiram = {}  # Dicionário para armazenar os usuários que reagiram ao embed
        

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(923244743083819088)
        self.emojis = guild.emojis
        for e in self.emojis:
            if(e.name == 'dps'):
                dps = e
            if(e.name == 'support'):
                support = e
            if(e.name == 'healer'):
                healer = e
            if(e.name == 'tanker'):
                tanker = e
            if(e.name == 'try'):
                Tentativa = e
        emojis = {
            'dps': dps,
            'support': support,
            'healer': healer,
            'tanker': tanker,
            'Lista de Espera': Tentativa,
        }
        emoji_to_field = {
        emojis["dps"]: f'{emojis["dps"]} DPS',
        emojis["support"]:f'{emojis["support"]} Support',
        emojis["healer"]: f'{emojis["healer"]} Healer',
        emojis["tanker"]: f'{emojis["tanker"]} Tank',
        emojis["Lista de Espera"]: f'{emojis["Lista de Espera"]} Lista de Espera',
        }   

    @commands.hybrid_command(name="ping",description="Check if the bot is alive.",with_app_command=True,)
    async def ping(self, context: commands.Context) -> None:
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF,
        )
        await context.send(embed=embed, ephemeral=True)
                    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        if payload.event_type != 'REACTION_ADD':
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if not message.embeds:
            return

        emoji = str(payload.emoji)
        if emoji in emoji_to_field:
            if payload.user_id != self.bot.user.id:
                field_name = emoji_to_field[emoji]

                embed = message.embeds[0]
                # Extrai o tipo do título
                tipo = embed.title.split()[1]
                if field_name not in self.usuarios_reagiram:
                    self.usuarios_reagiram[field_name] = {}
                    
                if payload.user_id not in self.usuarios_reagiram[field_name]:
                    user = self.bot.get_user(payload.user_id)
                    if user:
                        self.usuarios_reagiram[field_name][payload.user_id] = user.mention
                        # Atualiza o campo personalizado correspondente ao emoji
                        for i, field in enumerate(embed.fields):
                            '''if user.mention in field.value:
                                await message.remove_reaction(emoji, discord.Object(payload.user_id))
                                return
                                '''
                            field_parts = field.name.split()
                            if field_parts[0] == emoji:
                                num_reacoes = len(self.usuarios_reagiram[field_name])
                                limit = limites[tipo][field_parts[1]]
                                '''if num_reacoes > limit:
                                    lista_usuarios = '\n'.join(self.usuarios_reagiram[f'{emojis["Lista de Espera"]} Lista de Espera'].values())
                                    lista_usuarios += f'\n{user.mention}'
                                    num_reacoes = len(self.usuarios_reagiram[f'{emojis["Lista de Espera"]} Lista de Espera'])+1
                                    new_field_name = f"{emojis['Lista de Espera']} Lista de Espera ({num_reacoes}/{limit})"
                                    embed.set_field_at(i, name=new_field_name, value=lista_usuarios, inline=True)
                                    return'''
                                new_field_name = f"{field_name} ({num_reacoes}/{limit})"
                                lista_usuarios = '\n'.join(self.usuarios_reagiram[field_name].values())
                                embed.set_field_at(i, name=new_field_name, value=lista_usuarios, inline=True)
                            

                        await message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload,):
        if payload.event_type != 'REACTION_REMOVE':
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if not message.embeds:
            return

        emoji = str(payload.emoji)
        if emoji in emoji_to_field:
            if payload.user_id != self.bot.user.id:
                field_name = emoji_to_field[emoji]

                embed = message.embeds[0]

                # Extrai o tipo do título
                tipo = embed.title.split()[1]

                if field_name in self.usuarios_reagiram and payload.user_id in self.usuarios_reagiram[field_name]:
                    del self.usuarios_reagiram[field_name][payload.user_id]

                    # Atualiza o campo personalizado correspondente ao emoji
                    for i, field in enumerate(embed.fields):
                        field_parts = field.name.split()
                        if field_parts[0] == emoji:
                            num_reacoes = len(self.usuarios_reagiram[field_name])
                            limit = limites[tipo][field_parts[1]]
                            new_field_name = f"{field_name} ({num_reacoes}/{limit})"
                            lista_usuarios = '\n'.join(self.usuarios_reagiram[field_name].values())
                            embed.set_field_at(i, name=new_field_name, value=lista_usuarios, inline=True)
                            break

                    await message.edit(embed=embed)

        
    @commands.hybrid_command(name='evento',description='Cria um evento novo',with_app_command=True,)
    @app_commands.choices(tipo=[
        app_commands.Choice(name="Fractal", value="Fractal"),
        app_commands.Choice(name="Strike", value="Strike"),
        app_commands.Choice(name="Raid", value="Raid"),
        app_commands.Choice(name="Meta", value="Meta"),
    ])
    @app_commands.choices(titulo=[
        app_commands.Choice(name="Treinamento", value="Treinamento"),
        app_commands.Choice(name="Panelinha", value="Panelinha"),
        app_commands.Choice(name="CM", value="CM"),
    ])
    @app_commands.describe(subtitulo="entre com o subtitulo do evento")
    @app_commands.describe(descricao="entre com a descrição do evento")
    @app_commands.describe(data="entre com a data no formato dd/mm")
    @app_commands.describe(horario="entre com o horario no formato hh:mm, eg: 16:05")
    @app_commands.describe(duracao="entre com a duração do evento em minutos eg: 30m eg: 2h")
    @app_commands.describe(requerimentos="entre com os requerimentos do evento")
    async def evento(
        self,
        ctx: commands.Context,
        tipo: app_commands.Choice[str],
        titulo: app_commands.Choice[str],
        subtitulo: str,
        descricao: str,
        data: str,
        horario: str,
        duracao: str,
        requerimentos: str,
    ) -> None:
        
        tipo = tipo.value
        titulo = titulo.value
        tiptit = f"{tipo} {titulo}"
        
        data = data.split('/')
        data = datetime.date(2023, int(data[1]), int(data[0]))
        data = data.strftime("%d/%m/%Y")

        horario = horario.split(':')
        if 0 <= int(horario[0]) <= 23:
            horario.append('00')
            horario = datetime.time(int(horario[0]), int(horario[1]), 0, 0, None)
            horario = horario.strftime("%H:%M")
        else:
            await ctx.send('Horario invalido', ephemeral=True)

        def create_embed():
            embed = discord.Embed(
                title=f"🗓️ {tiptit}",
                description=subtitulo,
                color=0xff0000
            )
            embed.add_field(name="Commander: ", value=f"{ctx.author.mention}", inline=False)
            embed.add_field(name="Descrição", value=descricao, inline=False)
            embed.add_field(name="Data e hora", value=f"{data} {horario}", inline=False)
            embed.add_field(name="Duração", value=duracao, inline=False)
            embed.add_field(name="Requerimentos", value=requerimentos, inline=False)
            embed.add_field(name=f'{emojis["dps"]} DPS (0/{limites[tipo]["DPS"]})', value=f'vagas:{limites[tipo]["DPS"]}', inline=True)
            embed.add_field(name=f'{emojis["support"]} Support (0/{limites[tipo]["Support"]})', value=f'vagas:{limites[tipo]["Support"]}', inline=True)
            embed.add_field(name=f'{emojis["healer"]} Healer (0/{limites[tipo]["Healer"]})', value=f'vagas:{limites[tipo]["Healer"]}', inline=True)
            if tipo == 'Raid' or tipo == 'Strike' or tipo == 'Meta':
                embed.add_field(name=f'{emojis["tanker"]} Tank (0/{limites[tipo]["Tank"]})', value=f'vagas:{limites[tipo]["Tank"]}', inline=True)
            embed.add_field(name=f'{emojis["Lista de Espera"]} Lista de Espera (0/{limites[tipo]["Lista de Espera"]})', value="talvez eu apareça aqui", inline=True)
            embed.set_footer(text="--------------")
            return embed

        emoji_list = ["<:dps:1151585351631114290>","<:support:1151585350347657420>","<:healer:1151588279985119282>","<:try:1151585352780353588>"]
        emoji_list1 = ["<:dps:1151585351631114290>","<:support:1151585350347657420>","<:healer:1151588279985119282>","<:tanker:1151585347399073832>","<:try:1151585352780353588>"]

        if tipo == 'Fractal' or tipo == 'Strike':
            embed = create_embed()
            mess = await ctx.send(embed=embed)
            for emoji in emoji_list:
                await mess.add_reaction(emoji)
        elif tipo == 'Raid' or tipo == 'Meta':
            embed = create_embed()
            mess = await ctx.send(embed=embed)
            for emoji in emoji_list1:
                await mess.add_reaction(emoji)
        else:
            await ctx.send('Tipo de evento não suportado', ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(Evento(bot))
    logger.info("Cog loaded: Evento")