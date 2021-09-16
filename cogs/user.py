import pycord
from pycord import user
from pycord.ext import commands

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import config

# Firebase Setup
cred = credentials.Certificate(config.FIREBASE_PRIVATEKEY)
firebase_admin.initialize_app(cred, {
    'databaseURL': config.DATABASE_URL
})

class User():
    def __init__(self) -> None:
        pass

    async def create_user(user: pycord.Member):
        data = {
            user.id:{
                'econ-bank': 0,
                'econ-wallet': 0,
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

    async def create_staff_account(user: pycord.Member):
        # Ranks:
        # 0 = Trainee
        # 1 = Moderator
        # 2 = Sr. Mod
        # 3 = Admin
        # 4 Sr. Admin
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
    
    async def delete_user(user: pycord.Member):
        ref = db.reference(f"/{user.id}")
        ref.delete()


class Users(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='createuser')
    async def _create_user(self, ctx: commands.Context, member: pycord.Member):
        await User.create_user(member)
        await ctx.send(f"Created account for {member.mention}")
    
    @commands.command(name='deleteuser')
    async def _delete_user(self, ctx: commands.Context, member: pycord.Member):
        await User.delete_user(user=member)
        ctx.send(f"Deleted account for {member.display_name}!")
    
    @commands.command(name='addstaff')
    async def _add_staff(self, ctx: commands.Context, member: pycord.Member):
        await User.create_staff_account(member)
        await ctx.send(f'Added {member.mention} to the staff team! <a:rave_parrot:886489050624692235>')

def setup(bot):
    bot.add_cog(Users(bot))

def get_name():
    return "Users"