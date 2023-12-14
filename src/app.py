import json
import logging
import typing as t

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery

from core.config import settings
from polls import enums, managers, utils

app = Client(
    settings.project_name,
    api_id=settings.api_id.get_secret_value(),
    api_hash=settings.api_hash.get_secret_value(),
    bot_token=settings.bot_token.get_secret_value(),
)


@app.on_message(filters.command("start") & filters.private)
async def start_pet_advisor(client, message):
    await message.reply(message.text)


@app.on_message(filters.command("help") & filters.private)
async def help_pet_advisor(client, message):
    await message.reply(message.text)


@app.on_callback_query(filters.private)
async def poll_pet_advisor(client: Client, callback: CallbackQuery):
    # retrieve machine 4 dialog & user
    try:
        user_id = str(callback.from_user.id)
        chat_id = str(callback.chat_instance) if callback.chat_instance else "0"
        callback_data: dict[str, t.Any] = json.loads(callback.data)
        machine = await managers.get_by_ids(user_id, chat_id)

        answer = None
        # parse user input
        await machine.next(user_input=message.text)
        if machine.state != enums.PetAdvisorStatesEnum.RESULT:
            results = await machine.get_result()
            for result in results:
                await message.reply(*utils.transform_2_tg_answer(result))
        else:
            answer = await machine.get_dialog_step()
        if not answer:
            return
        await message.reply(*utils.transform_2_tg_answer(answer))

    except Exception as e:
        logging.error(e)
        return


app.run()  # Automatically start() and idle()
