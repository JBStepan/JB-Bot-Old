import json
from os import name

import discord
from discord.ext import commands

async def setupuser(user: discord.Member, json_file: str):
    with open(json_file, 'r') as file:
        users = json.load(file)

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]['level'] = 1
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['perm_infractions'] = 0
        users[str(user.id)]['bank'] = 0.00
        users[str(user.id)]['wallet'] = 100.00
        users[str(user.id)]['items'] = []

    with open(json_file, 'w') as file:
        users['users'].append(users)
        json.dump()
    
    return True

async def removeuser(user: discord.Member, json_file: str):
    with open(json_file, 'r') as file:
        users = json.load(file)
    
    del users[str(user.id)]

    with open(json_file, 'w'):
        json.dump(users, file, indent=4)

class Users(commands.Cog, name='Users'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.jsondb = 'persistent_data/users.json'

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await setupuser(member, self.jsondb)

    @commands.Cog.listener()
    async def on_member_leave(member):
        await removeuser(member, 'persistent_data/users.json')

    @commands.command(name='adduser')
    async def _add_user(self, ctx, user: discord.Member):
        with open('persistent_data/users.json', 'r') as file:
            users = json.load(file)

        if user.id in users:
            await ctx.send('User already exsits!')
        else:
            users[user.id] = {}
            users[user.id]['experience'] = 0
            users[user.id]['perm_infractions'] = 0
            users[user.id]['bank'] = 0.00
            users[user.id]['wallet'] = 100.00
            users[user.id]['items'] = []

        with open('persistent_data/users.json', 'w') as file:
            json.dump(users, file, indent=4)
        await ctx.send(f'Completed user setup for @{user}!')

def setup(bot):
    bot.add_cog(Users(bot))