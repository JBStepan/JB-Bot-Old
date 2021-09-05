import discord
from discord.ext import commands

from bot_settings import *

class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(member):
        new_user = {"id": member.id, "exp": 0, "level": 0, "money": 100, "items": []}
        users.insert_one(new_user)
        print(f'Created account for {member.display_name}.')
    
    @commands.Cog.listener()
    async def on_member_remove(member):
        users.delete_one({"id": member.id})
        print(f'Removed account for {member.display_name}.')
    
    # Creates an account for the member given
    # Args:
    #   member: 
    #       The member to create an account for.
    @commands.command()
    async def create(self, ctx, member: discord.Member=None):
        new_user = {"id": member.id, "exp": 0, "level": 0, "money": 100, "items": []}
        users.insert_one(new_user)
        print(f'Created account for {member.display_name}.')
        await ctx.send(f"Created account for {member.mention}!")

def setup(bot):
    bot.add_cog(Users(bot))