import discord
from discord.ext import commands

# Other import
import cogs.econ

COG_NAME = 'Help'

# Cog variables
help_accepted_perams = ["econ"]
help_plugins = {
    "econ": cogs.econ.help_embed()
}

# Cog Class
class Help(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='help')
    async def _help(self, ctx: commands.Context, plugin: str=""):        
        if plugin in help_accepted_perams:
            await ctx.send(embed=help_plugins[plugin.lower()])
        elif plugin == "":
            embed_general = discord.Embed(title="JB Bot Plugin Commands")
            embed_general.add_field(name='**Economy**', value="`$help econ`")
            embed_general.add_field(name='**Levels**', value="`$help levels`")
            await ctx.send(embed=embed_general)
        else:
            embed_error = discord.Embed(description="**Error**: No plugin found!")
            await ctx.send(embed=embed_error)
            

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Help(bot))

def get_name():
    return COG_NAME