from typing import List
import discord

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from config import *

cred = credentials.Certificate(firebase_cred)

firebase_admin.initialize_app(cred, {
    'databaseURL': databaseurl
})


class EconAccount():
    def __init__(self, wallet, bank, items) -> None:
        self.wallet = wallet
        self.bank = bank
        self.items = items

class User():
    def __init__(self) -> None:
        pass
    
    async def has_any_role(member: discord.Member, roles=[]):
        if roles == []:
            return 

    # Database Functions
    def create_user(user: discord.Member):
        data = {
            "econ-bank": 0,
            "econ-wallet": 0,
            "econ-items": [],
            "leveling-level": 1,
            "leveling-exp": 1,
            "mod-amountkicks": 0,
            "mod-amountwarns": 0,
            "mod-amountmutes": 0
        }
        ref = db.reference(f'/{user.id}')
        ref.set(data)
        
        
    
    async def delete_user(user: discord.Member):
        ref = db.reference(f'/{user.id}')
        ref.delete()

    ########
    # Econ #
    ########

    # Retrives the bank data of someone
    async def get_bank_data(member: discord.Member):
        wallet, bank= db.reference(f'/{member.id}/econ-wallet'), db.reference(f'/{member.id}/econ-bank')

        i = wallet.get(shallow=True)
        j = bank.get(shallow=True)

        return EconAccount(i, j, None)
    
    
    async def give_money(member: discord.Member, amount: float):
        """Gives the given amount of money to someones wallet"""
        ref = db.reference(f'/{member.id}/econ-wallet')

        k = ref.get() + amount

        ref.set(k)
    
    # When called the amount will be taken away from the users wallet and added to their bank
    async def deposit_money(member: discord.Member, amount: float):
        wallet, bank = db.reference(f'/{member.id}/econ-wallet'), db.reference(f'/{member.id}/econ-bank')

        i = wallet.get() - amount
        j = bank.get() + amount

        wallet.set(i)
        wallet.set(j)

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
        ref = db.reference(f'/{user.id}')
        ref.update(data)
    
    async def promote_staff(user: discord.Member, rank: int):
        ref = db.reference(f'/{user.id}/staff-account')

        ref.update({'rank': rank})
    # Mod updates
    async def give_ban(banned: discord.Member, banner: discord.Member, reason: str):
        pass
