from turtle import color
import discord
from discord.ext import commands

from utils.help import cog_help

class FakeNitroView(discord.ui.View):
    def __init__(self, msg: discord.Message, ctx: commands.Context):
        super().__init__(timeout=30)
        self.msg = msg
        self.ctx = ctx
    
    @discord.ui.button(label="Claim!", style=discord.ButtonStyle.blurple)
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description=f"You can't claim that nitro {interaction.user.mention}", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        button.label = "Claimed!"
        button.style = discord.ButtonStyle.danger
        button.disabled = True
        await interaction.response.send_message(content="https://imgur.com/NQinKJB", ephemeral=True)
        embed = discord.Embed(description=f"{self.ctx.author.mention} claimed free Nitro!!!!")
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)
    
class ConfirmView(discord.ui.View):
    def __init__(self, msg: discord.Message, ctx: commands.Context, member: discord.Member):
        super().__init__(timeout=30)
        self.msg = msg
        self.ctx = ctx
        self.memner = member
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description=f"You can't", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        button.label = "Confirmed"
        button.style = discord.ButtonStyle.danger
        button.disabled = True
        await interaction.response.send_message(content="User kicked", ephemeral=True)
        embed = discord.Embed(description=f"{self.ctx.author.mention} kicked {self.memner.display_name}", color=discord.Color.green())
        await self.memner.kick()
        await self.msg.edit(embed=embed, view=self)

    async def on_timeout(self) -> None:
        await self.msg.delete()
        await self.ctx.send("Timed out!")
    
class HelpOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, row=1)
    async def delete_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
    
    @discord.ui.select(
        placeholder="Select a category",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Fun",
                description="View all fun commands"
            ),
            discord.SelectOption(
                label="Moderation",
                description="View all Mod commands"
            )
        ]
    )
    async def options_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0]:
            await interaction.response.edit_message(
                embed=discord.Embed(
                    title=f"{select.values[0]} Help!",
                    description=cog_help[select.values[0]],
                    color=discord.Color.blue()
                )
            )
