import motor.motor_asyncio
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
db_url = config.get('mongodb', 'db_url')
owner = config.get('owner', 'owner')
owner_username = f'@{config.get("owner", "owner_username")}'
connect = motor.motor_asyncio.AsyncIOMotorClient(db_url)
create = connect.neko

users = create.users
messages = create.messages
bans = create.bans

async def get_message_id(message_id):
	message_id = await messages.find_one({'message_id_forward': f'{message_id}'})
	return message_id
