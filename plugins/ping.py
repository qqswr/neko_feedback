from pyrogram import Client, filters
from pyrogram.types import Message
from time import perf_counter
from .utils import owner


@Client.on_message(filters.command(['ping', 'p']) & filters.chat(int(owner)), group=-1)
async def ping(client: Client, message: Message):
    start = perf_counter()
    message = await message.reply('Pong')
    end = perf_counter()
    ping = end - start
    await message.edit(f'<b>Ping</b><code> {round(ping, 3)}s</code>')
    message.stop_propagation()

