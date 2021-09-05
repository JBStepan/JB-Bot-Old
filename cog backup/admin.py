import discord
from discord.ext import commands
import typing

class Admin(commands.Cog, name='Admin Commands Cog'):
    def __init__(self, bot):
        self.bot = bot

    # Bans a user for a given reason
    # Args:
    #   members: 
    #       The members you want to ban!
    #   delete_days:
    #       The amount of days you would like to ban the person for. Defualt is 0.
    #   reason:
    #       The reason why they have been banned.
    @commands.command('ban')
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member, delete_days: typing.Optional[int] = 0, *, reason: str = 'No reasons given'):
        role = discord.utils.get(ctx.guild.roles, name="Not Bannable")
        if role in member.roles:
            await ctx.send('Unable to ban someone who is unbannable! Tried to ban {0}.'.format(member))
        else:
            # bans the user
            await member.ban(delete_message_days=delete_days, reason=reason) 
            # Send a message in the channel where the command was given
            await ctx.send('Member @{0} has been banned!! For reason {1}!!'.format(member, reason))
            # Send the baned user a DM.
            channel = await member.create_dm()
            await channel.send('You have been banned from the server! For the reason of {0}'.format(reason))
                       
    # Kick a user for a given reason
    # Args:
    #   members: 
    #       The members you want to Kick!
    #   reason:
    #       The reason why they have been kicked.
    @commands.command('kick')
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason: str = 'No reasons given'):
        role = discord.utils.get(ctx.guild.roles, name="Not Bannable")
        if role in member.roles:
            await ctx.send('Unable to kick someone who is unkickable! Tried to kick {0}.'.format(member))
        else:
            # kicks the user
            await member.kick(reason=reason)
            # send a message in the channel the command was used
            await ctx.send('Member @{0} has been kicked!! For reason {1}!!'.format(member, reason))
            # send the kicked user a dm
            channel = await member.create_dm()
            await channel.send('You have been kicked from the server! For the reason of {0}'.format(reason))  
    
    # Warns a user for the given reason
    # Args:
    # member:
    #   The member that should be warned
    # severity:
    # How bad the infraction should be: low, medium or high
    @commands.command('warn')
    @commands.has_role('staff')
    async def _warn(self, ctx, member: discord.Member, severity):
        if severity == 'low':
            member_dm = member.create_dm()
            


def setup(bot):
    bot.add_cog(Admin(bot))