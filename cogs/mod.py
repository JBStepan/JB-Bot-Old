import re
import discord
from discord.errors import DiscordException
from discord.ext import commands

from bot_settings import *

class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    # Removes the given amount of messages from a channel
    # Args:
    #   ammount: 
    #       The ammount of messages you would like to delete.
    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx: commands.Context, ammount:int=10):
        if ammount <= 50:
            await ctx.message.delete()
            await ctx.channel.purge(limit=ammount)
            await ctx.send(f"Deleted {ammount} messages!", delete_after=3.0)
        else:
            embed = discord.Embed(title="Error!", color=discord.Color.red())
            embed.add_field(name="Error Message: ", value="Unable to delete more than 50 messages!")
            await ctx.send(embed=embed)

    # Warns the given member for the given reason
    # Args:
    #   member: 
    #       The you would like to warn.
    #   reason:
    #       The reason you warned the person.
    @commands.command(name="warn")
    @commands.has_role("Staff")
    async def _warn(self, ctx: commands.Context, member: discord.Member, reason: str="None given"):
        # Get the users account data
        user_account = users.find_one({"id": member.id})
        new_infraction = user_account['mod-infraction-count'] + 1
        new_infraction_details = (reason, ctx.author.display_name)
        users.update_one({"id": member.id}, {"$set":{'mod-infraction-count':new_infraction}})
        users.update_one({"id": member.id}, {"$push":{"mod-infractions": new_infraction_details}})

        # Create warning DM
        embed = discord.Embed(title="You have been warned!", color=discord.Color.blue())
        embed.add_field(name="Warner: ", value=f"{ctx.author.display_name}", inline=False)
        embed.add_field(name="Reason: ", value=f"`{reason}`", inline=False)
        await member.send(embed=embed)
        await ctx.send(f"You have warned {member.display_name} for {reason}")
        
        # Sending a message to #spam-logs
        spam_logs = discord.channel.utils.get(ctx.author.guild.channels, id=881619827406561367)
        embed = discord.Embed(title=f"{member.display_name} has been warned!", color=discord.Color.green())
        embed.add_field(name="Person Warned: ", value=f"{member.display_name}", inline=False)
        embed.add_field(name="Warned by: ", value=f"{ctx.author.display_name}", inline=False)
        embed.add_field(name="Reason: ", value=f"`{reason}`", inline=False)
        await spam_logs.send(embed=embed)

    @commands.command(name="kick")
    async def _kick(self, ctx: commands.Context, member: discord.Member, reason: str="None given"):
        await member.kick(reason=reason)
        await member.send(f"You have been kicked! For: {reason}")

def setup(bot):
    bot.add_cog(Moderator(bot))