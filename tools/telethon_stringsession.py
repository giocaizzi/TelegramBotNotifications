import asyncio
from telethon import TelegramClient
import decouple
from telethon.sessions import StringSession


API_ID=decouple.config("TELEGRAM_API_ID")
API_HASH=decouple.config("TELEGRAM_API_HASH")
PASSWORD=decouple.config("TELEGRAM_2FA_PASSWORD")

client=TelegramClient(StringSession(), API_ID, API_HASH)

async def telegram_user():
    # await client.connect()
    await client.sign_in(password=PASSWORD)
    print("Signed in.")
    print(client.session.save())
    print("Session saved.")

with client:
    client.loop.run_until_complete(telegram_user())