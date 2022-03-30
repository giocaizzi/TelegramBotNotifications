"""
test telegram bot
"""
import pytest
from unittest.mock import patch
import asyncio
import pytest_asyncio
import telegram
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import decouple
import pandas as pd
import random, string
import time 

from TelegramBotNotifications import TelegramBot

TOKEN = decouple.config("TELEGRAM_TOKEN")
API_ID = decouple.config("TELEGRAM_API_ID")
API_HASH = decouple.config("TELEGRAM_API_HASH")
PASSWORD = decouple.config("TELEGRAM_2FA_PASSWORD")
STRINGSESSION = decouple.config("TELETHON_STRINGSESSION")
USER_ID = decouple.config("TELEGRAM_USER_ID")


@pytest.fixture
async def telegram_user(request):
    """user to interact with bot programmatically"""
    client = TelegramClient(StringSession(STRINGSESSION), API_ID, API_HASH)

    async def init():
        await client.connect()
        return client

    yield await init()

    def finalizer():
        client.disconnect()

    request.addfinalizer(finalizer)

def test_init_testbot():
    """initialize default class"""
    t = TelegramBot(TOKEN)
    assert t.token == TOKEN
    assert t.channel_mode is False
    assert isinstance(t.bot, telegram.Bot)
    isinstance(t.updates, pd.DataFrame)

def test_init_testbot_channelmode():
    """initialize default class channel mode but without specifing path"""
    with pytest.raises(ValueError):
        t = TelegramBot(TOKEN,channel_mode=True)

@pytest.mark.asyncio
async def test_init_testbot_and_get_updates(telegram_user):
    """send unique text to bot and process updates correctly"""

    # fixture
    client = telegram_user

    # it fills the entity cache.
    dialogs = await client.get_dialogs()
    entity = await client.get_entity("surfingcrypto_test_bot")

    unique_test_message = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
    )
    await client.send_message(entity=entity, message=unique_test_message)

    t = TelegramBot(TOKEN)
    assert len(t.updates) > 0
    assert unique_test_message in t.updates["message"].tolist()

@pytest.mark.asyncio
async def test_send_message_and_photo(telegram_user):
    """send unique text to bot and a photo and process updates correctly"""
    t = TelegramBot(TOKEN)

    unique_test_message = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
    )
    t.send_message(unique_test_message, USER_ID)
    #it was the easieast to store it there given fixture
    t.send_photo("docsrc/source/images/logo.png",USER_ID)
    
    time.sleep(1)

    client = telegram_user
    # fetch id of user interacting with bot
    async for dialog in client.iter_dialogs():
        if dialog.name == "surfingcrypto_testbot":
            entity = dialog.entity
            break
    found_photo,found_message=False,False
    async for message in client.iter_messages(entity):
        if message.media is not None:
            found_photo= True
        if str(message.message) == unique_test_message:
            found_message = True
    
    assert found_message is True
    assert found_photo is True

# @pytest.mark.parametrize(
#     "temp_test_env", [("config_telegram.json",)], indirect=["temp_test_env"]
# )
# def test_fail_send_message(temp_test_env):
#     """fail send message"""
#     t = TelegramBot(TOKEN)
#     assert len(t.error_log)==0
#     t.send_message("FAILED MESSAGE", 0000000)
#     assert isinstance(t.error_log[0],dict)

# @pytest.mark.parametrize(
#     "temp_test_env", [("config_telegram.json",)], indirect=["temp_test_env"]
# )
# def test_fail_send_photo(temp_test_env):
#     """fail send photo"""
#     t = TelegramBot(TOKEN)
#     assert len(t.error_log)==0
#     t.send_photo(str("config"/"logo.jpg"), 0000000)
#     assert isinstance(t.error_log[0],dict)

# @patch.object(telegram.Bot,"sendMessage") 
# @pytest.mark.parametrize(
#     "temp_test_env", [("config_telegram.json","telegram_users.csv")], indirect=["temp_test_env"]
# )
# def test_message_to_all(mock_getter,temp_test_env):
#     """send message to all stored contacts, without updates"""
#     t = TelegramBot(TOKEN,channel_mode=True,new_users_check=False)
#     t.send_message_to_all("fail")
#     assert mock_getter.call_count == 3

# @pytest.mark.skip
# @patch.object(telegram.Bot,"send_photo") 
# @pytest.mark.parametrize(
#     "temp_test_env", [("config_telegram.json","telegram_users.csv","logo.jpg")], indirect=["temp_test_env"]
# )
# def test_photo_to_all(mock_getter,temp_test_env):
#     """send photo to all stored contacts, without updates"""
#     root = temp_test_env
#     c = Config(str(root / "config"))
#     t = TelegramBot(c,channel_mode=True,new_users_check=False)
#     t.send_photo_to_all(str(root/"config"/"logo.jpg"))
#     assert mock_getter.call_count == 3

