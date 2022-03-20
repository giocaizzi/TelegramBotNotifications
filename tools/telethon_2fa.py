import asyncio
from telethon import TelegramClient
import decouple

API_ID=decouple.config("TELEGRAM_API_ID")
API_HASH=decouple.config("TELEGRAM_API_HASH")
PASSWORD=decouple.config("TELEGRAM_2FA_PASSWORD")

client=TelegramClient('anon', API_ID, API_HASH)

async def telegram_user():
    await client.connect()
    if not await client.is_user_authorized():
    # Sets new password with recovery email:
        try:
            client.edit_2fa(new_password=PASSWORD,
                            email='giocaizzi@gmail.com')
            # Raises error (you need to check your email to complete 2FA setup.)
        except:
            # You can put email checking code here if desired.
            raise NotImplementedError

with client:
    client.loop.run_until_complete(telegram_user())