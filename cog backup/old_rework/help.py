from unicodedata import name
import discord
from discord.ext import commands

# Other import
import cogs.marriage

COG_NAME = 'Help'
enabled = True

# Cog variables
help_accepted_perams = ["econ"]
help_plugins = {
    
}

# Cog Class
class Help(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='help')
    async def _help(self, ctx: commands.Context, plugin: str=""):        
        # If the plugin is in the plugin help list give the help embed
        if plugin in help_accepted_perams:
            await ctx.send(embed=help_plugins[plugin.lower()])
        # Else give the user general help
        elif plugin == "":
            # If the user has Trainee Mod role or above, send them this
            embed_general = discord.Embed(title="JB Bot Plugin Commands")
            embed_general.add_field(name='**Economy**', value="`$help econ`")
            await ctx.send(embed=embed_general)

            if ctx.author().guild_permissions.administrator == True:
                mod_embed = discord.Embed(title="Moderator Commands")
                mod_embed.add_field(name="**User Management**", value="`$help user`")
                mod_embed.add_field(name="**Channel Management**", value="`$help channel`")
                
                await ctx.send(embed=mod_embed)
        else:
            embed_error = discord.Embed(description="**Error**: No plugin found!", color=discord.Color.red())
            await ctx.send(embed=embed_error)
            

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Help(bot))

def get_name():
    return COG_NAME