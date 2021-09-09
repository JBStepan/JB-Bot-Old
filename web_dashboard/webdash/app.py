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
    return render_template("index.html")

@app.route("/sendmessage", methods=["GET", "POST"])
def send_message():
    if request.method == "POST":
        req = request.form
        
        roleid = request.form["role"]
        content = request.form["content"]

        for role in jb_world_server.roles:
            if role.id == roleid:
                for member in role.members:
                    dm = member.create_dm()
                    dm.send(content=content)
        
        return redirect(url_for("send_message"))

    return render_template("send_message.html")