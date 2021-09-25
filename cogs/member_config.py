import discord
from discord.embeds import EmptyEmbed
from discord.ext import commands
from discord.ui import view

# Other import

COG_NAME = 'MemberConfig'

# Cog variables
class VerifyButton(discord.ui.View):
    @discord.ui.button(label='Verify', style=discord.ButtonStyle.green, custom_id='button:serververify', emoji='✅')
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        verifyrole = discord.utils.find(lambda e: e.name == 'Verified', interaction.guild.roles)
        await interaction.user.add_roles(verifyrole)
        userdm = await interaction.user.create_dm()
        await userdm.send('You have been verified!')

# Cog Class
class MemberConfig(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.persistent_views_added = False

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added == False:
            self.bot.add_view(VerifyButton(timeout=None))
            self.persistent_views_added = True

    # Commands 
    @commands.is_owner()
    @commands.command(name='setupverify')
    async def setup_verify(self, ctx: commands.Context):
        embed = discord.Embed(title='Verification', description='Once you have read <#881619826764812300> and <#886639447909736478> \n\n You can click on the button below to be verified!')
        view = VerifyButton(timeout=None)
        await ctx.send(embed=embed, view=view)
    # Helper Functions

    # Any other function

def setup(bot):
    bot.add_cog(MemberConfig(bot))

def get_name():
    return COG_NAME