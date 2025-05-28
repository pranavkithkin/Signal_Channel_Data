from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel
import re
import pandas as pd
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

def extract_signals_from_channel(channel_id, access_hash, months_back, limit=None, session_name="anon"):
    """
    Extracts signals from a Telegram channel and returns a pandas DataFrame.
    """
    client = TelegramClient(session_name, api_id, api_hash)

    async def main():
        await client.start(phone_number)
        channel = InputPeerChannel(channel_id, access_hash)
        start_date = datetime.now(timezone.utc) - relativedelta(months=months_back)
        all_messages = []
        async for message in client.iter_messages(channel, limit=limit):
            text = None
            if hasattr(message, 'message') and message.message:
                text = message.message.strip()
            elif hasattr(message, 'caption') and message.caption:
                text = message.caption.strip()
            if text and message.date and message.date >= start_date:
                match = re.search(r"#(\w+)\s+(bullish|bearish)", text, re.IGNORECASE)
                if match:
                    coin = match.group(1).upper()
                    direction = match.group(2).capitalize()
                    timestamp = message.date
                    all_messages.append({
                        'timestamp': timestamp,
                        'coin': coin,
                        'direction': direction,
                        'raw_message': text
                    })
        return pd.DataFrame(all_messages)

    # --- Robust event loop handling for Flask threads ---
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        return loop.run_until_complete(main())
    else:
        return asyncio.run(main())