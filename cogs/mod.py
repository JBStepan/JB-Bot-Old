from email import message
import discord
from discord.ext import commands
from utils.views import ConfirmView

# # Other import
import config
import asyncio


COG_NAME = 'Moderator'
enabled = True

# # Cog variables
muted_people = []

# # Cog Class
class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

# Events

# Commands 

    # modslash = discord.SlashCommandGroup("Moderator Commands", "Things for mods", config.DEBUG_GUILDS)

    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context, amount: int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages! <a:rave_parrot:886489050624692235>", delete_after=2)

    # @modslash.command(description="Clears the current channel of the given amount of messages", guild_ids=[883774092505940019])
    # async def __clear(self, ctx: discord.ApplicationContext, amount: int):
    #     await ctx.message.delete()
    #     await ctx.channel.purge(limit=amount)
    #     await ctx.send(f"Cleared {amount} messages! <a:rave_parrot:886489050624692235>", delete_after=2)

    @commands.command(name="warn")
    async def _warn(self, ctx: commands.Context, member: discord.Member, *, reason: str=None):
         print(f"{ctx.message.author.display_name} has warned {member.display_name} for, {reason}")
         await ctx.message.delete()

         embed = discord.Embed(title="You have been warned!")
         embed.color = discord.Color.red()
         embed.add_field(name="Reason", value=reason)
         embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar.url)

         await member.send(embed=embed)
    
    @commands.command(name="kick")
    async def _kick(self, ctx: commands.Context, member: discord.Member, *, reason: str=None):
        print(f"{ctx.message.author.display_name} has kicked {member.display_name} for, {reason}")
        embed = discord.Embed(description=f"Are you sure? \n You have 30 seconds to respond", color=discord.Color.red())
        
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=ConfirmView(message, ctx, member))

    @commands.command(name='mute')
    async def _mute(self, ctx: commands.Context, user: discord.Member, reason):
        print(f"{ctx.message.author.display_name} has muted {user.display_name} for, {reason}")
        


#     # Helper Functions

#     # Any other function

def setup(bot):
     bot.add_cog(Moderator(bot))

def get_name():
     return COG_NAME