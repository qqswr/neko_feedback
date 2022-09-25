from pyrogram import Client, filters
from pyrogram.types import Message
from .utils import owner, bans


@Client.on_message(filters.command(['ban', 'b']) & filters.chat(int(owner)), group=0)
async def ban(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.forward_from.id
    elif len(message.command) > 1:
        user_id = message.command[1]

    user = {'user': f'{user_id}'}
    await bans.insert_one(user)
    await message.reply_text(f"<b>You blocked <code>{user_id}</code></b>", reply_to_message_id=message.message_id)
    await client.send_message(user_id, "<b>Your account has been banned!</b>")


@Client.on_message(filters.command(['unban', 'unb']) & filters.chat(int(owner)), group=0)
async def unban(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.forward_from.id
    elif len(message.command) > 1:
        user_id = message.command[1]

    await bans.delete_many({'user': f'{user_id}'})
    await message.reply_text(f"<b>You unblocked user <code>{user_id}</code></b>", reply_to_message_id=message.message_id)
    await client.send_message(user_id, "<b>Your account is unbanned!</b>")