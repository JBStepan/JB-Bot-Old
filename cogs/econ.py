import datetime
import discord
from discord.ext import commands

# Other import
from cogs.user import User

COG_NAME = 'Economy'

# Cog variables

# Cog Class
class Economy(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='bal')
    async def _bal(self, ctx: commands.Context):
        account_data = await User.get_bank_data(member=ctx.author)

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Balance")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(name=f"Wallet: ", value=f'{account_data.wallet}')
        embed.add_field(name=f"Bank: ", value=f'{account_data.bank} / **{account_data.maxbank}**')
        await ctx.send(embed=embed)

    @commands.command(name='givemoney')
    async def _give_money(self, ctx: commands.Context, member: commands.MemberConverter, amount: float):
        await User.give_money(member, amount)
        await ctx.send(f"Gave {amount} to {member.display_name}")

    @commands.command(name='deposit')
    async def _deposit(self, ctx: commands.Context, amount):
        float_amount = float(amount)
        await User.deposit_money(ctx.author, float_amount)
        await ctx.send(f"Deposited {amount} into your bank!")

    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(Economy(bot))

def get_name():
    return COG_NAME