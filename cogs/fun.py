import discord
from discord.ext import commands

# Other import
from utils.views import FakeNitroView

COG_NAME = 'Fun'
enabled = True

# Cog variables

# Cog Class
class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='nitro')
    async def _nitro(self, ctx: commands.Context):
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=FakeNitroView(message, ctx))

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Fun(bot))

def get_name():
    return COG_NAME

def help_embed():
    embed = discord.Embed(title="Template Pugin", description="""
    `$command`
    A really cool command!
    """)
    return embed