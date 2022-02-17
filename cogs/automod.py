import discord
from discord.ext import commands

# Other import
import config

COG_NAME = 'Automod'
enabled = True

# Cog variables

# Cog Class
class Automod(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            pass
        else:
            message_content = message.content
            for badword in config.BANNED_WORDS:
                if badword in message_content:
                    await message.delete()
    # Commands 

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Automod(bot))

def get_name():
    return COG_NAME
