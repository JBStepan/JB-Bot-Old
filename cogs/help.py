import discord
from discord.ext import commands

# Other import
from utils.views import HelpOptions

COG_NAME = 'Help'
enabled = True

# Cog variables

# Cog Class
class Help(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name="help")
    async def _help(self, ctx: commands.Context):
        await ctx.send("Help", view=HelpOptions())

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Help(bot))

def get_name():
    return COG_NAME