import web_dashboard.webdash.app as app

def start_dash(bot, port=5000):
    app.start(bot, port)