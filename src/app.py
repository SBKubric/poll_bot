import json
import logging
import typing as t

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message

from core.config import settings
from polls import enums, managers, utils

app = Client(
    settings.project_name,
    api_id=settings.api_id.get_secret_value(),
    api_hash=settings.api_hash.get_secret_value(),
    bot_token=settings.bot_token.get_secret_value(),
)


@app.on_message(filters.command("start") & filters.private)
async def start_new_poll(client: Client, message: Message):
    if not message.chat.id:
        return

    user_id: str = str(message.from_user.id)
    chat_id: str = str(message.chat.id)
    poll = await managers.start_new_poll(user_id, chat_id)
    dialog_step = await poll.get_dialog_step()
    reply_markup = utils.transform_2_inline_markup(dialog_step.extras)
    if not reply_markup:
        logging.error("No reply markup")
        return

    if dialog_step.image_path:
        await client.send_photo(
            chat_id,
            photo=dialog_step.image_path,
            caption=dialog_step.message_txt,
            reply_markup=reply_markup,
        )
    await client.send_message(
        chat_id, dialog_step.message_txt, reply_markup=reply_markup
    )


@app.on_message(filters.command("stop") & filters.private)
async def stop_poll(client, message):
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id) if message.chat else "0"
    await managers.stop_poll_by_ids(user_id, chat_id)
    await message.reply(chat_id, "Ладно, я закончил")


@app.on_message(filters.command("help") & filters.private)
async def help_pet_advisor(client, message):
    await message.reply(
        "/help - get help\n/start - start new poll\n/stop - stop current poll"
    )


@app.on_callback_query(filters.private)
async def poll_pet_advisor(client: Client, callback: CallbackQuery):
    # retrieve machine 4 dialog & user
    if not callback.chat_instance:
        return
    try:
        user_id = str(callback.from_user.id)
        chat_id = str(callback.chat_instance)
        callback_data: dict[str, t.Any] = json.loads(callback.data)
        poll = await managers.get_by_ids(user_id, chat_id)

        answer = None
        # parse user input
        await poll.next(user_input=callback_data.get("ans"))

        if poll.state == enums.PetAdvisorStatesEnum.RESULT:
            await callback.answer("Ваши результаты теста:\n")
            results = await poll.get_results()
            for result in results:
                if result.image_path:
                    await client.send_photo(
                        chat_id, result.image_path, caption=result.message_txt
                    )
                    continue
                else:
                    await client.send_message(chat_id, result.message_txt)
                    continue
            return

        answer = await poll.get_dialog_step()
        reply_markup = utils.transform_2_inline_markup(answer.extras)
        if reply_markup:
            await client.send_message(
                chat_id, text=answer.message_txt, reply_markup=reply_markup
            )
            return
        await callback.answer(text=answer.message_txt)

    except Exception as e:
        logging.error(e)
        return


app.run()  # Automatically start() and idle()
