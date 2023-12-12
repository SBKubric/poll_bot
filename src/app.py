from pyrogram import filters
from pyrogram.client import Client

from core.config import settings

app = Client(
    settings.project_name,
    api_id=settings.api_id.get_secret_value(),
    api_hash=settings.api_hash.get_secret_value(),
    bot_token=settings.bot_token.get_secret_value(),
)


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)


app.run()  # Automatically start() and idle()
