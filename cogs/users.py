import discord
from discord.ext import commands

from bot_settings import *

class Users(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Helper commands
    def remove_user(self, member: discord.Member): 
        users.delete_one({"id": member.id})
        print(f'Removed account for {member.display_name}.')
    
    def create_user(self, member: discord.Member):
        new_user = {"id": member.id, "exp": 0, "level": 0, "money": 100, "items": [], "mod-infractions": [], "mod-infraction-count": 0}
        users.insert_one(new_user)
        print(f'Created account for {member.display_name}.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
       self.create_user(member)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.remove_user(member)
    
    # Creates an account for the member given
    # Args:
    #   member: 
    #       The member to create an account for.
    @commands.command(name='createaccount')
    async def create(self, ctx, member: discord.Member):
        self.create_user(member)
        await ctx.send(f"Created account for {member.mention}!")

    # Removes the account for the member given
    # Args:
    #   member: 
    #       The member to remove the account from.
    @commands.command(name='deleteaccount')
    async def delete_account(self, ctx, member: discord.Member):
        self.remove_user(member)
        await ctx.send(f"Removed account for {member.mention}!")

def setup(bot):
    bot.add_cog(Users(bot))