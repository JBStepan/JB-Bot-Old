from datetime import datetime
from typing import List
import discord

from config import *

import json


class EconAccount():
    def __init__(self, wallet, bank, items) -> None:
        self.wallet = wallet
        self.bank = bank
        self.items = items

class User():
    def __init__(self) -> None:
        pass
    
    # Database Functions
    def create_user(user: discord.Member):
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
        
        users[str(user.id)] = {}
        users[str(user.id)]["econ-bank"] = 0
        users[str(user.id)]["econ-wallet"] = 100
        users[str(user.id)]["econ-items"] = {}
        users[str(user.id)]["leveling-level"] = 1
        users[str(user.id)]["leveling-exp"] = 0
        users[str(user.id)]["mod-amountkicks"] = 0
        users[str(user.id)]["mod-amountwarns"] = 0
        users[str(user.id)]["mod-amountmutes"] = 0

        with open(USERS_JSON, 'w') as f:
            json.dump(users, f, indent=4)
        
    
    async def delete_user(user: discord.Member):
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
        
        users.pop(str(user.id))

        with open(USERS_JSON, 'w') as f:
            json.dump(users, f, indent=4)

    ########
    # Econ #
    ########

    # Retrives the bank data of someone
    async def get_bank_data(member: discord.Member):
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
        
        wallet = users[str(member.id)]["econ-wallet"]
        bank = users[str(member.id)]["econ-bank"]
        items = users[str(member.id)]["econ-items"]

        return EconAccount(wallet, bank, items)
    
    async def open_account(member: discord.Member):
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
        
        return users[str(member.id)]
    
    async def give_money(member: discord.Member, amount: float):
        """Gives the given amount of money to someones wallet"""
        pass
    
    # When called the amount will be taken away from the users wallet and added to their bank
    async def deposit_money(member: discord.Member, amount: float):
        pass
    
    async def buy_item(member: discord.Member, price: float):
        pass

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
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
        
        users[str(user.id)]["staff-account"] = {} 
        users[str(user.id)]["staff-account"]["rank"] = 0
        users[str(user.id)]["staff-account"]["amount-bans"] = 0
        users[str(user.id)]["staff-account"]["amount-kicks"] = 0
        users[str(user.id)]["staff-account"]["amount-warns"] = 0
        users[str(user.id)]["staff-account"]["amount-mutes"] = 0

        with open(USERS_JSON, 'w') as f:
            json.dump(users, f, indent=4)
    
    async def promote_staff(user: discord.Member, rank: int):
       pass
    
    #########
    # Staff #
    #########
    async def give_ban(banned: discord.Member, banner: discord.Member, reason: str, ban_id: str):
        with open(BAN_JSON, 'r') as f:
            bans = json.load(f)

        if str(banner.id) not in bans:
            time = datetime.now()
            strtime = datetime.strftime(time, '%m/%d/%Y')
            bans["bans"][str(banned.id)] = {'banner': banner.id, 'reason': reason, 'banid': str(ban_id), 'timeofban': strtime, 'bantimes': 1}
        else:
            bans["bans"][str(banned.id)]['bantimes'] += 1
        
        with open(BAN_JSON, 'w') as f:
            json.dump(bans, f, indent=4)

