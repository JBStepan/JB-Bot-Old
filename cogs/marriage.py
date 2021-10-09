import discord
from discord.ext import commands
from discord.user import User

from cogs.cogimports.users import User

# Other import

COG_NAME = 'Marriage'
enabled = True

# Cog variables

# Cog Class
class Marriage(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command("marry")
    async def _marry(self, ctx: commands.Context, member: discord.Member):
        await User.marry_users(ctx.author, member)
        await ctx.send(f"I now pronoce you to be married, {ctx.author.mention} and {member.mention}!")

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Marriage(bot))

def get_name():
    return COG_NAME

def help_embed():
    embed = discord.Embed(title="Econ Plugin", description="""
    `$command`
    A really cool command!
    """)
    return embed