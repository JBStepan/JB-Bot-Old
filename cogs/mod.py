import pycord
from pycord.ext import commands

class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context, amount: int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages! <a:rave_parrot:886489050624692235>", delete_after=2)


def setup(bot):
    bot.add_cog(Moderator(bot))

def get_name():
    return "Moderator"