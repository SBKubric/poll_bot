import typing as t

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def transform_2_inline_markup(extras: dict[str, t.Any]) -> InlineKeyboardMarkup | None:
    if not extras.get("buttons"):
        return None
    buttons = []
    for key, value in extras.get("buttons", {}).items():
        buttons.append(InlineKeyboardButton(text=value, callback_data=key))
    return InlineKeyboardMarkup([buttons])
