from pyrogram import Client, idle


app = Client("neko_bot")

if __name__ == '__main__':
    app.start()
    idle()
