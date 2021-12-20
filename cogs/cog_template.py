import discord
from discord.ext import commands

# Other import

COG_NAME = 'Cog name here'
enabled = True

# Cog variables

# Cog Class
class CogName(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(CogName(bot))

def get_name():
    return COG_NAME

def help_embed():
    embed = discord.Embed(title="Template Pugin", description="""
    `$command`
    A really cool command!
    """)
    return embed