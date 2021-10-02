import datetime
import discord
from discord.ext import commands

# Other import
from cogs.user import User

COG_NAME = 'Economy'

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
    def __init__(self, type: int, id: str, name: str, price: float, description: str, canbedestroyed: bool, useable_item: bool, *, role=None, icon=None):
        self.type = type
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.canbedestroyed = canbedestroyed
        self.useable_item = useable_item
        if role != None:
            self.role = role
        if icon != None:
            self.icon = icon

    def get_item_from_string(string: str):
        for i in range(len(shop)):
            if shop[i].id == string:
                return shop[i]

shop = [
    Item(1, "goldrole", "Gold Role", 100.00, "Role of the Gold", canbedestroyed=False, useable_item=False, role=887826427074981949), 
    Item(0, "watch", "Watch", 25.00, "Tells the time (24 hour format)", canbedestroyed=True, useable_item=True),
    Item(1, "dj", "DJ Role", 1500.00, "Gives acsess to JB Music and MEE6 music commands.", False, True, role=886494118115680298)
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
            embed.add_field(name=f'{shop[i].name} - ${str(shop[i].price)}', value=f'{shop[i].description}\n `{shop[i].id}`', inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='buy')
    async def _buy(self, ctx: commands.Context, item_id: str):
        """Buys the given item"""
        item_to_buy = Item.get_item_from_string(item_id)
        if item_to_buy is not None:
            await self.buy_item(item_to_buy, ctx.author, ctx)
            await ctx.send(f'{ctx.author.display_name} just bought {item_to_buy.name}')
        else:
            await ctx.send('That item does not exist!')
    
    @commands.command(name='debugbuy')
    async def _debug_buy(self, ctx: commands.Context, item_id: str):
        """Buys the given item"""
        item_to_buy = Item.get_item_from_string(item_id)
        if item_to_buy is not None:
            await self.debug_buy_item(item_to_buy, ctx.author, ctx)
            await ctx.send(f'{ctx.author.display_name} just bought {item_to_buy.name}')
        else:
            await ctx.send('That item does not exist!')

    @commands.command(name='use')
    async def _use(self, ctx: commands.Context, item_id: str, action=None):
        """Uses the given specified item"""
        item = item_id.lower()
        item_to_user = Item.get_item_from_string(item)
        if item_to_user != None:
            if item_to_user.useable_item == True:
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
            role = discord.utils.find(lambda m: m.id == item.role, ctx.guild.roles)
            await User.buy_item(ctx.author, item.price)
            await member_buying.add_roles(role)
        else:
            await ctx.send('Debugging, only roles can be purchased now')
    
    async def debug_buy_item(self, item: Item, member_buying: discord.Member, ctx: commands.Context):
        if item.type == 1:
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