import discord
from discord.ext import commands

# Other import
import config

COG_NAME = 'Automod'

# Cog variables

# Cog Class
class AutomodCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(AutomodCog(bot))

def get_name():
    return COG_NAME