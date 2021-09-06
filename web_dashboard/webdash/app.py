from flask import Flask, request, url_for, redirect, render_template
import threading
from discord.ext import commands


bot = None
command_prefix = None
jb_world_server = None

app = Flask(__name__)

def start(init_bot: commands.Bot, port: int=5000):
    global bot
    global command_prefix
    global jb_world_server

    bot = init_bot

    command_prefix = bot.command_prefix

    jb_world_server = bot.guilds[0]

    threading.Thread(target=app.run, kwargs={ 'port': port }).start()

@app.route("/")
def index():
    return render_template("index.html", command_prefix=command_prefix, server_name=jb_world_server.name, roles=jb_world_server.roles)