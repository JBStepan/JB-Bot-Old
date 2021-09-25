import discord
from discord.ext import commands

from cogs.cogimports.users import *

class Users(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(member: discord.Member):
        User.create_user(member)
    
    # Create account in the database for the spesified member
    @commands.command(name='createuser')
    async def _create_user(self, ctx: commands.Context, member: discord.Member):
        User.create_user(member)
        await ctx.send(f"Created account for {member.mention}")
    
    # Delete a user from the member given
    @commands.command(name='deleteuser')
    async def _delete_user(self, ctx: commands.Context, member: discord.Member):
        await User.delete_user(user=member)
        ctx.send(f"Deleted account for {member.display_name}!")
    
    # Add a member to the staff team
    @commands.command(name='addstaff')
    @commands.has_permissions(administrator=True)
    async def _add_staff(self, ctx: commands.Context, member: discord.Member):
        await User.create_staff_account(member)
        await ctx.send(f'Added {member.mention} to the staff team! <a:rave_parrot:886489050624692235>')
    
    # Promotes a staff member to the new rank
    @commands.command(name='promotestaffmember')
    @commands.has_permissions(administrator=True)
    async def _promote_staff_member(self, ctx: commands.Context, member: discord.Member, rank: int):
        await User.promote_staff(member, rank)
        await ctx.send(f'Promoted {member.mention}! <a:rave_parrot:886489050624692235>')

def setup(bot):
    bot.add_cog(Users(bot))

def get_name():
    return "Users"