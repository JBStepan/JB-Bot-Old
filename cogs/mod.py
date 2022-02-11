from unicodedata import name
import discord
from discord.ext import commands

# Other import
import config


COG_NAME = 'Moderator'
enabled = True

# Cog variables

# Cog Class
class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context, amount: int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages! <a:rave_parrot:886489050624692235>", delete_after=2)

    @commands.command(name="warn")
    async def _warn(self, ctx: commands.Context, member: discord.Member, *, reason: str=None):
        await ctx.message.delete()

        embed = discord.Embed(title="You have been warned!")
        embed.color = discord.Color.red()
        embed.add_field(name="Reason", value=reason)
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar.url)

        print("Ok")
        await member.send(embed=embed)
    
    @commands.command(name="kick")
    async def _kick(self, ctx: commands.Context, member: discord.Member, *, reason: str=None):
        await ctx.message.delete()
        
        

        embed = discord.Embed(title="You've been kicked!")
        embed.color = discord.Color.red()
        embed.add_field(name="Reason", value=reason)
        embed.description = "Since you've been kicked you can rejoin. But if you are kick 3 times that is a ban!"
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.display_avatar.url)

        await member.send(embed=embed)
        await member.kick()

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Moderator(bot))

def get_name():
    return COG_NAME

def help_embed():
    embed = discord.Embed(title="Template Pugin", description="""
    `$command`
    A really cool command!
    """)
    return embed