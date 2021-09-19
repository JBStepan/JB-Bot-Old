import discord
from discord import user
from discord.ext import commands

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

import config

# Firebase Setup
cred = credentials.Certificate(config.FIREBASE_PRIVATEKEY)
firebase_admin.initialize_app(cred, {
    'databaseURL': config.DATABASE_URL
})

class EconAccount():
    def __init__(self, wallet, bank, items, maxbank) -> None:
        self.wallet = wallet
        self.bank = bank
        self.items = items
        self.maxbank = maxbank

class User():
    def __init__(self) -> None:
        pass
    
    async def create_user(user: discord.Member):
        data = {
            user.id:{
                'econ-bank': 0,
                'econ-wallet': 0,
                'econ-maxbank': 5000,
                'leveling-level': 1,
                'leveling-exp': 1,
                'mod-amountbans': 0,
                'mod-amountkicks': 0,
                'mod-amountwarns': 0,
                'mod-amountmutes': 0
            }
        }
        ref = db.reference(f"/")
        ref.update(data)
    
    async def delete_user(user: discord.Member):
        ref = db.reference(f"/{user.id}")
        ref.delete()

    ########
    # Econ #
    ########

    # Retrives the bank data of someone
    async def get_bank_data(member: discord.Member):
        wallet, bank, maxbank = db.reference(f"/{member.id}/econ-wallet"), db.reference(f"/{member.id}/econ-bank"), db.reference(f"/{member.id}/econ-maxbank")

        i = wallet.get(shallow=True)
        j = bank.get(shallow=True)
        k = maxbank.get(shallow=True)

        return EconAccount(i, j, None, k)
    
    # Gives the amount of money to someone
    async def give_money(member: discord.Member, amount: float):
        account = db.reference(f"/{member.id}")
        wallet = db.reference(f"/{member.id}/econ-wallet")

        i = wallet.get() + amount

        account.update({"econ-wallet": i})
    
    # When called the amount will be taken away from the users wallet and added to their bank
    async def deposit_money(member: discord.Member, amount: float):
        account = db.reference(f"/{member.id}")
        wallet = db.reference(f"/{member.id}/econ-wallet")
        bank = db.reference(f"/{member.id}/econ-bank")

        i = wallet.get() - amount
        j = bank.get() + amount

        account.update({
            "econ-wallet": i,
            "econ-bank": j
        })

    #########
    # Staff #
    #########
    async def create_staff_account(user: discord.Member):
        # Ranks:
        # 0 = Trainee
        # 1 = Moderator
        # 2 = Sr. Mod
        # 3 = Admin
        # 4 = Sr. Admin
        # 5 = Owner
        data = {
            'staff-account': {
                'rank': 0,
                'amount-bans': 0,
                'amount-kicks': 0,
                'amount-warns': 0,
                'amount-mutes': 0
            }
        } 
        ref = db.reference(f"/{user.id}")
        ref.update(data)
    
    async def promote_staff(user: discord.Member, rank: int):
        ref = db.reference(f"/{user.id}/staff-account")
        ref.update({'rank': rank})
    
    # Mod updates
    async def give_ban(banned: discord.Member, banner: discord.Member, reason: str):
        staffmember = db.reference(f"/{banner.id}/staff-account/")
        staffmemberbans = db.reference(f"/{banner.id}/staff-account/amount-bans")
        bannedmemberbans = db.reference(f"/{banned.id}/mod-amountbans")
        bannedmember = db.reference(f"/{banned.id}")

        i = staffmemberbans.get() + 1
        j = bannedmemberbans.get() + 1

        staffmember.update({'amount-bans': i})
        bannedmember.update({'mod-amountbans': j})

    


class Users(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(member: discord.Member):
        await User.create_user(member)
    
    # Create account in the database for the spesified member
    @commands.command(name='createuser')
    async def _create_user(self, ctx: commands.Context, member: discord.Member):
        await User.create_user(member)
        await ctx.send(f"Created account for {member.mention}")
    
    # Delete a user from the member given
    @commands.command(name='deleteuser')
    async def _delete_user(self, ctx: commands.Context, member: discord.Member):
        await User.delete_user(user=member)
        ctx.send(f"Deleted account for {member.display_name}!")
    
    # Add a member to the staff team
    @commands.command(name='addstaff')
    @commands.has_permissions(administrator=True)
    async def _add_staff(self, ctx: commands.Context, member: discord.Member):
        await User.create_staff_account(member)
        await ctx.send(f'Added {member.mention} to the staff team! <a:rave_parrot:886489050624692235>')
    
    # Promotes a staff member to the new rank
    @commands.command(name='promotestaffmember')
    @commands.has_permissions(administrator=True)
    async def _promote_staff_member(self, ctx: commands.Context, member: discord.Member, rank: int):
        await User.promote_staff(member, rank)
        await ctx.send(f'Promoted {member.mention}! <a:rave_parrot:886489050624692235>')

def setup(bot):
    bot.add_cog(Users(bot))

def get_name():
    return "Users"