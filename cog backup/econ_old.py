import json

import discord
from discord.ext import commands

class Economy(commands.Cog, name='Economy'):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='add-money')
    @commands.has_role('Banker')
    async def _add_money(self, ctx, member: commands.MemberConverter, amount: float, wallet: str='false'):
        with open('persistent_data/users.json') as file:
            users = json.load(file)
        
        if wallet == 'false':
            users[str(member.id)]['wallet'] += amount
        else:
            users[str(member.id)]['bank'] += amount

        with open('persistent_data/users.json') as file:
            json.dump(users, file, indent=4)
        await ctx.send(f'Added {amount} to {member}s account!')

    @commands.command(name='balance')
    async def _balance(self, ctx, member: discord.Member):
        pass


def setup(bot):
    bot.add_cog(Economy(bot))