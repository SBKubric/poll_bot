import asyncio
import logging

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import (
    BotCommand,
    CallbackQuery,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

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
    await client.set_bot_commands(  # type: ignore
        commands=[
            BotCommand("start", "Start new poll"),
            BotCommand("stop", "Stop current poll"),
            BotCommand("help", "Get help"),
        ]
    )

    if not message.chat.id:
        return

    user_id: str = str(message.from_user.id)
    chat_id: str = str(message.chat.id)

    await client.send_message(
        chat_id,
        text="Привет, это бот, который может помочь тебе с выбором домашнего питомца.",
    )
    try:
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
    except Exception as e:
        logging.error(e)


@app.on_message(filters.command("stop") & filters.private)
async def stop_poll(client, message):
    try:
        if not message.chat.id:
            logging.error("message.chat.id is None")
            return
        user_id = str(message.from_user.id)
        chat_id = str(message.chat.id)
        await managers.stop_poll_by_ids(user_id, chat_id)
        await message.reply("Ладно, я закончил")
    except Exception as e:
        logging.error(e)


@app.on_message(filters.command("help") & filters.private)
async def help_pet_advisor(client, message):
    await message.reply(
        "/help - get help\n/start - start new poll\n/stop - stop current poll"
    )


@app.on_callback_query()
async def poll_pet_advisor(client: Client, callback: CallbackQuery):
    # retrieve machine 4 dialog & user
    if not callback.chat_instance:
        return
    try:
        user_id = str(callback.from_user.id)
        chat_id = str(callback.message.chat.id)
        if type(callback.data) != str:
            logging.error("callback.data is not str")
            return
        callback_data: str = callback.data
        poll = await managers.get_by_ids(user_id, chat_id)

        answer = None
        # parse user input
        await poll.next(user_input=callback_data)

        if poll.state == enums.PetAdvisorStatesEnum.RESULT:
            await client.send_message(chat_id, text="Ваши результаты теста:\n")
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
            logging.info("trying to send message to {}".format(chat_id))
            await client.send_message(
                chat_id, text=answer.message_txt, reply_markup=reply_markup
            )
            return
        await callback.answer(text=answer.message_txt)

    except Exception as e:
        logging.error(e)
        return


app.run()
