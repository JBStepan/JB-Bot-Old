import random

import discord
from discord import embeds
from discord.colour import Color
from discord.ext import commands

from bot_settings import *

# Fun roles

class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == 884301918090956891:
            one_message = discord.utils.get(message.guild.roles, id=884305519416864769)
            await message.author.add_roles(one_message)
            print(f"{message.author.display_name} has used their on message!")

    @commands.command(name="serverinfo")
    async def _server_info(self, ctx: commands.Context):
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.add_field(name="Total Members: ", value=f"{ctx.guild.member_count} Members", inline=False)
        embed.set_footer(text=f"ID: {ctx.guild.id} | Created on: {ctx.guild.created_at}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="coinflip", aliases=['flip'])
    async def _coin_flip(self, ctx):
        flip = random.randint(0, 1) 
        embed = discord.Embed(color=Color.gold())
        if flip == 0:
            embed.title = "It was heads! :coin:"
            print("Heads")
        elif flip == 1:
            embed.title = "It was tails! :coin:"
            print("Tails")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))