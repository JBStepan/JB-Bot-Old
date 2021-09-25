import datetime
import typing

import discord
from discord.ext import commands

# Other import
from cogs.user import User

COG_NAME = 'Economy'

# Cog variables

# Item Dict
#   type - What is them items function. useable=0, role=1 and consumable=2
#   name - What is the items name.
#   price - What is the items price.
#   description - What does this item do
#   canbedestoryed - If the item can be destroyed by the user
#   onuse(optional) - If this is a useable item, this will be called
#   role(optional) - If this is a role item, the role will be given to the person. Use role id
#   onconsume(optional) - If this is a consumable item, this will be called

shop = [
    {"type": 0, "name": "Watch", "price": 30.00, "description": "Tells time", "canbedestroyed": True, "onuse": f"The time is {datetime.datetime.now()}"},
    {"type": 1, "name": "Gold Role", "price": 100.00, "description": "Gives you the gold role!", "canbedestroyed": False, "role": 887826427074981949},
    {"type": 2, "name": "Banana", "price": 15.00, "description": "Gives to potasium", "canbedestroyed": True, "onconsume": "{user} just ate a banana"}
]

# Cog classes
class Item():
    def __init__(self, type: int, name: str, price: float, description: str, canbedestroyed: bool, *, onuse=None, role=None, onconsume=None):
        self.type = type
        self.name = name
        self.price = price
        self.description = description
        self.canbedestroyed = canbedestroyed
        if onuse != None:
            self.onuse = onuse
        if role != None:
            self.role = role
        if onconsume != None:
            self.onconsume = onconsume
    
    def to_dict():
        item = {}
        
        

# Cog Class
class Economy(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Events

    # Commands 
    @commands.command(name='bal')
    async def _bal(self, ctx: commands.Context):
        """Shows the person how much money they have"""
        account_data = await User.get_bank_data(member=ctx.author)

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Balance", description=f"**Wallet**: ⏣{account_data.wallet} \n **Bank**: ⏣{account_data.bank}")
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
    async def buy_item(item, member_buying: discord.Member):
        ...

    # Any other function

def setup(bot):
    bot.add_cog(Economy(bot))

def get_name():
    return COG_NAME