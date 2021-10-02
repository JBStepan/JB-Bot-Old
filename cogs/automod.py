import discord
from discord.ext import commands

import config
# Other import

COG_NAME = 'Automod'

# Cog variables
banned_words = ['fuck', 'shit']

def check_banned_words(message: str=None):
    for i in message.split():
        if i in config.BANNED_WORDS:
            return True
        else:
            return False

# Cog Class
class AutoMod(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        i = check_banned_words(message.content)
        if i == True:
            await message.delete()
            await message.channel.send('Watch you fucking swearing!', delete_after=2)
    # Commands 

    # Helper Functions
    
    # Any other function

def setup(bot):
    bot.add_cog(AutoMod(bot))

def get_name():
    return COG_NAME