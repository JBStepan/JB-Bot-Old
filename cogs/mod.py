import discord
from discord.ext import commands

from cogs.user import User

import config

import uuid

enabled = True

class Moderator(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='clear')
    async def _clear(self, ctx: commands.Context, amount: int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount} messages! <a:rave_parrot:886489050624692235>", delete_after=2)
    
    @commands.command(name='mute')
    async def _mute(self, ctx: commands.Context, member: discord.Member, *, args):
        mutedrole = discord.utils.find(lambda e: e.name == "Muted", ctx.guild.roles)
        await member.add_roles(mutedrole)

        embed = discord.Embed(title=f"Muted {member.display_name}", color=discord.Color.red())
        embed.add_field(name='Muted by: ', value=ctx.author.display_name)
        embed.add_field(name='Reason: ', value=args)
        
        embed2 = discord.Embed(title="You have been muted!", color=discord.Color.red())
        embed2.add_field(name='Muted by: ', value=ctx.author.display_name)
        embed2.add_field(name='Reason: ', value=args)

        userdm = await member.create_dm()
        await ctx.send(embed=embed)
        await userdm.send(embed=embed2)
    
    # Bans the given user for a given reason
    @commands.command(name='ban')
    async def _ban(self, ctx: commands.Context, member: discord.Member, delete_message_days: int=1, *, args):
        """Bans the given user for a given reason"""
        # Do some behind the scenes stuff
        await member.ban(delete_message_days=delete_message_days, reason=args)
        ban_id = uuid.uuid1()
        await User.give_ban(member, ctx.author, args, ban_id)

        # Messages
        ctx_embed = discord.Embed(title=f"{ctx.author.display_name} has banned {member.display_name}", color=discord.Color.red())
        ctx_embed.set_thumbnail(url=member.display_avatar.url)
        ctx_embed.add_field(name='Delete Message Days', value=delete_message_days, inline=False)
        ctx_embed.add_field(name='Reason: ', value=args)
        ctx_embed.add_field(name='User id: ', value=member.id)

        embed = discord.Embed(title=f"You have been banned!", color=discord.Color.red())
        embed.add_field(name="Reason: ", value=args, inline=False)
        embed.add_field(name="Banned by: ", value=ctx.author.display_name)
        embed.add_field(name='Ban ID: ', value=str(ban_id), inline=False)
        embed.set_footer(text = f'You can appeal a ban here: https://forms.gle/BWH6pJ9JLZLcoXUG9')

        # Send the banned user a dm and send a message in the channel where the command was sent
        banneddm = await member.create_dm()
        await banneddm.send(embed=embed)
        await ctx.send(embed=ctx_embed)
    
    @commands.command(name='kick')
    async def _kick(self, ctx: commands.Context, member: discord.Member, *, args):
        """Kicks the given user for a reason"""
        await member.kick(reason=args)

        # Messages
        embed = discord.Embed(title=f'{ctx.author.display_name} has kicked {member.display_name}!', color=discord.Color.red())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name='Reason: ', value=args, inline=False)
        embed.add_field(name=f'User ID: ', value=member.id)

        embed_dm = discord.Embed(title='You have been kicked!', color=discord.Color.red())
        embed_dm.add_field(name='Reason: ', value=args, inline=False)
        embed_dm.add_field(name='Kicked by: ', value=ctx.author.display_name)

        # Send the mbeds
        userdm = await member.create_dm()
        await ctx.send(embed=embed)
        await userdm.send(embed=embed_dm)

    @commands.command(name='unban')
    async def _unban(self, ctx: commands.Context, user_id: int, *, args):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=args)

        embed = discord.Embed(title=f'{ctx.author.display_name} has unbanned {user.display_name}', color=discord.Color.yellow())
        embed.add_field(name='Reason: ', value=args)

        dm_embed = discord.Embed(title='You have been unbaned in JB\'s Rift!')
        dm_embed.add_field(name='Reason: ', value=args)
        dm_embed.add_field(name='Unbanned by: ', value=ctx.author.display_name)

        user_dm = await user.create_dm()
        await user_dm.send(embed=dm_embed)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderator(bot))

def get_name():
    return "Moderator"