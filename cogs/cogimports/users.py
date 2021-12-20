from datetime import datetime
from typing import Dict
import discord
import config

from config import *

import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(config.FIREBASE_CONFIG)
firebase_admin.initialize_app(cred)

db = firestore.client()

class EconAccount():
    def __init__(self, wallet, bank, roles, items: Dict) -> None:
        self.wallet = wallet
        self.bank = bank
        self.items = items
        self.roles = roles

class User():
    def __init__(self) -> None:
        pass
    
    # Database Functions
    def create_user(user: discord.Member):
        
        # users[str(user.id)] = {}
        # users[str(user.id)]["econ-bank"] = 0
        # users[str(user.id)]["econ-wallet"] = 100
        # users[str(user.id)]["econ-items"] = {}
        # users[str(user.id)]["leveling-level"] = 1
        # users[str(user.id)]["leveling-exp"] = 0
        # users[str(user.id)]["mod-amountkicks"] = 0
        # users[str(user.id)]["mod-amountwarns"] = 0
        # users[str(user.id)]["mod-amountmutes"] = 0

        data = {
            u"econ-bank": 0,
            u"econ-wallet": 100,
            u"econ-items": {},
            u"leveling-level": 1,
            u"leveling-exp": 0,
            u"mod-amountkicks": 0,
            u"mod-amountwarns": 0,
            u"mod-amountmutes": 0,
            u"staff-account": {}
        }

        db.collection(u'users').document(str(user.id)).set(data)
        
    
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
        roles = users[str(member.id)]["econ-roles"]

        return EconAccount(wallet, bank, roles, items)

    async def user_has_item(user: discord.User, item: str):
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)
        
        if item in users[str(user.id)]["econ-items"]:
            return True
        else:
            return False
    
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
    
    async def buy_item(member: discord.Member, price: float, is_role: bool, item=None, role=None):
        with open(USERS_JSON, 'r') as f:
            users = json.load(f)

        if item not in users[str(member.id)]["econ-items"]:
            users[str(member.id)]["econ-wallet"] -= price
            users[str(member.id)]["econ-items"][item] = 1
        else:
            users[str(member.id)]["econ-items"][item] += 1

        with open(USERS_JSON, 'w') as f:
            json.dump(users, f, indent=4)
    
    #######
    # Fun #
    #######
    async def marry_users(user1: discord.User, user2: discord.User):
        with open(MARRIAGE_JSON, 'r') as f:
            users = json.load(f)

        users[str(user1.id)] = {
            "married": str(user2),
            "level": 1,
            "level-xp": 0,
            "time": datetime.now()
        }

        users[str(user2.id)] = {
            "married": str(user1),
            "level": 1,
            "level-xp": 0,
            "time": datetime.now()
        }

        with open(MARRIAGE_JSON, 'w') as f:
            json.dump(users, f, indent=4)


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
        
        # users[str(user.id)]["staff-account"] = {} 
        # users[str(user.id)]["staff-account"]["rank"] = 0
        # users[str(user.id)]["staff-account"]["amount-bans"] = 0
        # users[str(user.id)]["staff-account"]["amount-kicks"] = 0
        # users[str(user.id)]["staff-account"]["amount-warns"] = 0
        # users[str(user.id)]["staff-account"]["amount-mutes"] = 0

        user = db.collection(u'users').document(str(user.id))
        user.update({u'staff-account': {
            "rank": 0,
            "amount-bans": 0,
            "amount-kicks": 0,
            "amount-warns": 0,
            "amount-mutes": 0
        }})
    
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

