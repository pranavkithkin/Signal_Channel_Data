from telethon.sync import TelegramClient

api_id = 1369657
api_hash = '58dee73868918be3ac7ba66e8754546b'
phone = +971589579932

client = TelegramClient('session_name', api_id, api_hash)

with client:
    for dialog in client.iter_dialogs():
        if dialog.is_channel:
            print(f"{dialog.name} | ID: {dialog.entity.id} | Access Hash: {dialog.entity.access_hash}")
