from pyrogram import Client, filters
from pyrogram.types import Message
from .utils import owner, owner_username, get_message_id, users, messages, bans
import asyncio


@Client.on_message(filters.command(['start']))
async def start(client: Client, message: Message):
    user_in_db = await users.find_one({'user': f'{message.from_user.id}'})
    ban_list = await bans.find_one({'user': f'{message.from_user.id}'})
    if not user_in_db:
        await message.reply_text(f'<b>Hello,  {message.from_user.mention}!</b>', reply_to_message_id=message.message_id)
        user = {'user': f'{message.from_user.id}'}
        await users.insert_one(user)
        await client.send_message(message.chat.id, f"<b>Send me your message and I'll forward it to {owner_username}.</b>")
    else:
        if not ban_list:
            await message.reply_text(f"<b>Send me your message and I'll forward it to {owner_username}.</b>", reply_to_message_id=message.message_id)
        else:
            await message.delete()


@Client.on_message(filters.chat(int(owner)))
async def admin_messages(client: Client, message: Message):
    last_msg = [_ async for _ in messages.find()][-1]
    if message.reply_to_message:
        if int(message.reply_to_message.from_user.id) != int(owner):
            message_id = await get_message_id(message_id=message.reply_to_message.message_id)
            await message.copy(int(message_id['user']), reply_to_message_id=int(message_id['message_id']))
            message = await message.reply_text(f"<b>Your message was delivered to {(message_id['user'])}</b>", reply_to_message_id=message.message_id)
            if int(last_msg['user']) != int(message_id['user']):
                message_data = {'message_id_forward': f"{message_id['message_id_forward']}",
                                'message_id': f"{message_id['message_id']}",
                                'user': f"{message_id['user']}"}
                await messages.insert_one(message_data)
            await asyncio.sleep(2)
            await message.delete()
        else:
            message_id = await get_message_id(message_id=last_msg['message_id_forward'])
            await message.copy(int(message_id['user']))
            message = await message.reply_text(f"<b>Your message was delivered to {(message_id['user'])}</b>", reply_to_message_id=message.message_id)
            await asyncio.sleep(2)
            await message.delete()

    else:
        message_id = await get_message_id(message_id=last_msg['message_id_forward'])
        await message.copy(int(message_id['user']))
        message = await message.reply_text(f"<b>Your message was delivered to {(message_id['user'])}</b>", reply_to_message_id=message.message_id)
        await asyncio.sleep(2)
        await message.delete()


@Client.on_message(filters.all & filters.private & ~filters.me)
async def all_messages(client: Client, message: Message):
    user_in_db = await users.find_one({'user': f'{message.from_user.id}'})
    ban_list = await bans.find_one({'user': f'{message.from_user.id}'})
    if not user_in_db:
        await message.reply_text(f"<b>You are not in the database, enter /start to use the bot!</b>", reply_to_message_id=message.message_id)
    else:
        if not ban_list:
            forwarded_message = await message.forward(owner)
            message_data = {'message_id_forward': f'{forwarded_message.message_id}',
                            'message_id': f'{message.message_id}',
                            'user': f'{message.from_user.id}'}
            await messages.insert_one(message_data)
            message = await message.reply_text(f"<b>Your message was delivered to {owner_username}</b>", reply_to_message_id=message.message_id)
            await asyncio.sleep(2)
            await message.delete()
        else:
            await message.delete()
