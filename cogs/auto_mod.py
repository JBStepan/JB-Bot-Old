import discord
from discord.ext import commands

from bot_settings import *

# AutoMod Catchers
bad_words = ['fuck', 'shit', 'cunt']

class AutoMod(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            pass
        else:
            message_content = message.content
            user_account = users.find_one({"id": message.author.id})
            for badword in bad_words:
                if badword in message_content:
                    await message.delete()
                    new_infraction = user_account['mod-infractions'] + 1
                    users.update_one({"id": message.author.id}, {"$set":{'mod-infractions':new_infraction}})
                    await message.channel.send(f"{message.author.mention} watch you profanity!")
                    break
    
    # Removes an infraction from the given user
    # Args:
    #   member: 
    #       The member to remove an infraction for.
    @commands.command(name='removeinfraction')
    @commands.has_role("Staff")
    async def _remove_infraction(self, ctx, member: discord.Member):
        user_account = users.find_one({"id": member.id})
        infractions = user_account['mod-infractions']
        if infractions > 0:
            removed_infraction = user_account['mod-infractions'] - 1
            users.update_one({"id": member.id}, {"$set":{'mod-infractions':removed_infraction}})
            await ctx.send(f"Removed infraction for {member.mention}!")
        else:
            await ctx.send(f"{member.display_name} already has 0 infractions!")

def setup(bot):
    bot.add_cog(AutoMod(bot))