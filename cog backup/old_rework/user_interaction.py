import discord
from discord.ext import commands

# Other import

COG_NAME = 'User Interactions'
enabled = True

# Cog variables

async def sendDM(self, user: discord.User, contents: str, file: discord.File = None, embed: discord.Embed=None):
    user.send(content=contents)

# Cog Class
class UserInteractions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='dm')
    async def _dm(self, user: discord.User, text: str):
        sendDM(self, user, text)

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(UserInteractions(bot))

def get_name():
    return COG_NAME

def help_embed():
    embed = discord.Embed(title="Template Pugin", description="""
    `$command`
    A really cool command!
    """)
    return embed