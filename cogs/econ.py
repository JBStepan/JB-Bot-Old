import datetime
import discord
from discord import role
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.commands import slash_command


# Other import
from cogs.user import User

COG_NAME = 'Economy'
enabled = True

# Cog classes
class Item():
    """Repersents an item that a person can buy \n
    \n
    Attributes:
    --------------
    `type` - What is them items function. useable=0 and role=1\n
    `id` - What is the items id. Used in the buy command\n
    `name` - What is the items name.\n
    `price` - What is the items price.\n
    `description` - What does this item do\n
    `canbedestoryed` - If the item can be destroyed by the user\n
    `useable_item` - If the item can be used\n
    `role(optional)` - If this is a role item, the role will be given to the person. Use role id\n
    Methods:
    -----------
    :meth:`get_item_from_string(string)` - Gets the items accocited with the string\n
    Example
    ------------
    ```py
    Item(0, 'example', 'Example Item', 100.00, 'Used for example', True, False)
    ```
    """
    def __init__(self, type: int, id: str, name: str, price: float, description: str, canbedestroyed: bool, useable_item: bool, icon: str):
        self.type = type
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.canbedestroyed = canbedestroyed
        self.useable_item = useable_item
        self.icon = icon

    def get_item_from_string(string: str):
        for i in range(len(shop)):
            if shop[i].id == string:
                return shop[i]

shop = [ 
    Item(0, "watch", "Watch", 25.00, "Tells the time (24 hour format)", canbedestroyed=True, useable_item=True, icon=':watch:'),
    Item(0, "ring", "Ring", 100.00, "A nice ring made with gold and diamonds. Used for a speical someone.", True, False, icon=":ring:"),
    Item(0, "goldpepe", "Golden Pepe", 25000000000.00, "Only for the richest of the richest", True, True, icon='<:goldenpepe:894352501241950248> ')
]

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

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Balance", description=f"**Wallet**: ${account_data.wallet} \n **Bank**: ${account_data.bank}")

        await ctx.send(embed=embed)
    
    @commands.slash_command()
    async def bal(self, ctx: commands.context):
        """Shows the person how much money they have"""
        account_data = await User.get_bank_data(member=ctx.author)

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Balance", description=f"**Wallet**: ${account_data.wallet} \n **Bank**: ${account_data.bank}")

        await ctx.send(embed=embed)

    @commands.command(name='givemoney')
    @commands.has_permissions(manage_emojis=True)
    async def _give_money(self, ctx: commands.Context, member: commands.MemberConverter, amount: float):
        """Gives the specified user the specified amount of money"""
        await User.give_money(member, amount)
        await ctx.send(f"Gave {amount} to {member.display_name}")

    @commands.command(name='deposit')
    async def _deposit(self, ctx: commands.Context, amount):
        """Deposits the given amount of money into the users bank"""
        float_amount = float(amount)
        await User.deposit_money(ctx.author, float_amount)
        await ctx.send(f"Deposited {amount} into your bank!")

    # Item related
    @commands.command(name='shop')
    async def _shop(self, ctx: commands.Context):
        """Displays all items that can be bought"""
        embed = discord.Embed(title='Shop Item', color=discord.Color.green())

        for i in range(len(shop)):
            embed.add_field(name=f'{shop[i].icon}  **{shop[i].name}** *{shop[i].id}* — ${str(shop[i].price)}', value=f'{shop[i].description}', inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='buy', aliases=['purchase'])
    async def _buy(self, ctx: commands.Context, item_id: str):
        """Buys the given item"""
        item_to_buy = Item.get_item_from_string(item_id)
        if item_to_buy is not None:
            await User.buy_item(ctx.author, item_to_buy.price, False, item_id)
            await ctx.send(f'{ctx.author.display_name} just bought {item_to_buy.name}')
        else:
            await ctx.send('That item does not exist!')
    
    @commands.command(name='inventory', aliases=['inv', 'items'])
    async def _inventory(self, ctx: commands.Context):
        items = await User.get_bank_data(ctx.author)
        if items.items:
            em = discord.Embed(title=f"{ctx.author.display_name}'s Inventory")

            for key, value in items.items.items():
                item = Item.get_item_from_string(key)
                em.add_field(name=f"**{item.name}**", value=value, inline=False)

            await ctx.send(embed=em)
    
    @commands.command(name='debugbuy')
    async def _debug_buy(self, ctx: commands.Context, item_id: str):
        """Buys the given item"""
        item_to_buy = Item.get_item_from_string(item_id)
        if item_to_buy is not None:
            await self.debug_buy_item(item_to_buy, ctx.author, ctx)
            await ctx.send(f'{ctx.author.display_name} just bought {item_to_buy.name}')
        else:
            await ctx.send('That item does not exist!')

    @commands.command(name='info')
    async def _info(self, ctx: commands.Context, item_id: str):
        item = Item.get_item_from_string(item_id)
        e = discord.Embed(title=f"{item.icon} {item.name}", description=item.description, color=colour.Color.blue())
        await ctx.send(embed=e)

    @commands.command(name='use')
    async def _use(self, ctx: commands.Context, item_id: str, action=None):
        """Uses the given specified item"""
        item = item_id.lower()
        item_to_user = Item.get_item_from_string(item)
        if item_to_user != None:
            if item_to_user.useable_item == True:
                # Gets the item id and throws it into a if loop from what todo, maybe make functions for each item
                if item_to_user.id == 'watch':
                    time = datetime.datetime.now()
                    strtime = datetime.datetime.strftime(time, "%H:%M")
                    em = discord.Embed(description=f"The current time is: **{strtime}**")
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="**Error**", description="That item does not exist!", color=discord.Color.red())
                    await ctx.send(embed=em)
            else:
                em = discord.Embed(title="**Error**", description="That item does is not usable!", color=discord.Color.red())
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title="**Error**", description="That item does is not exist!", color=discord.Color.red())
            await ctx.send(embed=em)

    # Helper Functions
    async def buy_item(self, item: Item, member_buying: discord.Member, ctx: commands.Context):
        if item.type == 1:
            pass
    
    async def debug_buy_item(self, item: Item, member_buying: discord.Member, ctx: commands.Context):
        if item.type == 1:
            role_ = item.id.upper()
            role = discord.utils.find(lambda m: m.id == item.role, ctx.guild.roles)
            await member_buying.add_roles(role)
        else:
            await ctx.send('Debugging, only roles can be purchased now')

    # Any other function

def setup(bot):
    bot.add_cog(Economy(bot))

def get_name():
    return COG_NAME

def help_embed():
    embed = discord.Embed(title="Econ Plugin", description="""
    `$bal`
    Gets you current wallet and bank balance

    `$shop`
    Opens the shop 

    `$deposit [amount]`
    Deposits a specified amount of money into your bank

    `$buy [item_id]`
    Buys the specified item.

    `$info [item_id]`
    Get info on the specified item.
    """)
    return embed