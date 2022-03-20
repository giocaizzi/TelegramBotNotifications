import asyncio
from telethon import TelegramClient
from telethon.errors import EmailUnconfirmedError
from telethon.sessions import StringSession
import decouple

API_ID=decouple.config("TELEGRAM_API_ID")
API_HASH=decouple.config("TELEGRAM_API_HASH")
PASSWORD=decouple.config("TELEGRAM_2FA_PASSWORD")
STRINGSESSION=decouple.config("TELETHON_STRINGSESSION")

client=TelegramClient(StringSession(STRINGSESSION), API_ID, API_HASH)

async def log_in():
    # fetch id of user interacting with bot
    async for dialog in client.iter_dialogs():
        if dialog.name == "surfingcrypto_testbot":
            entity = dialog.entity
            # chat_id = dialog.message.from_id.user_id #randomdly resitutes attribute error
            break
    async for message in client.iter_messages(entity):
        print(message)


with client:
    client.loop.run_until_complete(log_in())