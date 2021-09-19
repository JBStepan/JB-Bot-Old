import discord
from discord.ext import commands

from cogs.user import User

# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Confirming")
        self.value = True
        button.disabled = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling")
        button.disabled = True
        self.value = False
        self.stop()

class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context, amount: int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages! <a:rave_parrot:886489050624692235>", delete_after=2)
    
    @commands.command(name='ban')
    async def _ban(self, ctx: commands.Context, member: discord.Member, delete_message_days: int=1, reason: str='None given'):
        view = Confirm()
        await ctx.send(f"Are you sure you want to ban {member.display_name}?", view=view)

        await view.wait()
        if view.value is None:
            await ctx.send("Timed out!")
        elif view.value:
            # Do some behind the scenes stuff
            await member.ban(delete_message_days=delete_message_days, reason=reason)
            await User.give_ban(member, ctx.author, reason)

            # Messages
            ctx_embed = discord.Embed(title=f"{ctx.author.display_name} has banned {member.display_name}", color=discord.Color.red())
            ctx_embed.set_thumbnail(url=member.display_avatar.url)
            ctx_embed.add_field(name='Delete Message Days', value=delete_message_days, inline=False)
            ctx_embed.add_field(name='Reason: ', value=reason)
            ctx_embed.add_field(name='User id: ', value=member.id)

            embed = discord.Embed(title=f"You have been banned!", color=discord.Color.red())
            embed.add_field(name="Reason: ", value=reason, inline=False)
            embed.add_field(name="Banned by: ", value=ctx.author.display_name)

            banneddm = await member.create_dm()
            await banneddm.send(embed=embed)
            await ctx.send(embed=ctx_embed)
        else:
            await ctx.send("Canceled!")
        

def setup(bot):
    bot.add_cog(Moderator(bot))

def get_name():
    return "Moderator"