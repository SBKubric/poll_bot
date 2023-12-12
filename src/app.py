import logging

from pyrogram import filters
from pyrogram.client import Client

from core.config import settings

app = Client(
    settings.project_name,
    api_id=settings.api_id.get_secret_value(),
    api_hash=settings.api_hash.get_secret_value(),
    bot_token=settings.bot_token.get_secret_value(),
)


@app.on_message(filters.command("start") & filters.private)
async def start_pet_advisor(client, message):
    await message.reply(message.text)


@app.on_message(filters.command("stop") & filters.private)
async def stop_pet_advisor(client, message):
    await message.reply(message.text)


@app.on_message(filters.command("help") & filters.private)
async def help_pet_advisor(client, message):
    await message.reply(message.text)


@app.on_message(filters.text & filters.private)
async def poll_pet_advisor(client, message):
    # retrieve machine 4 dialog & user
    machine = None
    answer = None
    try:
        # parse user input
        await machine.next(user_input=message.text)
        if machine.state != enums.PetAdvisorStatesEnum.RESULT:
            answer = await machine.get_result()
        else:
            answer = await machine.get_dialog_step()
        if not answer:
            return
        await message.reply(2_tg_answer(answer))

    except Exception as e:
        logging.error(e)
        return
    await message.reply(message.text)


app.run()  # Automatically start() and idle()
