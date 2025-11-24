from pyrogram import filters
from pyrogram.types import Message, KeyboardButton, InlineKeyboardButton, CallbackQuery


def button_filter(button: KeyboardButton):
    async def func(_, __, update):
        # Guard: this filter is intended for Message updates only.
        # If update doesn't have `text`, return False safely.
        if not hasattr(update, "text"):
            return False
        return update.text == button.text

    return filters.create(func, "ButtonFilter", button=button)


def inline_button_filter(inline_button: InlineKeyboardButton):
    async def func(_, __, update):
        # Guard: this filter is intended for CallbackQuery updates only.
        # If update doesn't have `data`, return False safely.
        if not hasattr(update, "data"):
            return False
        return update.data == inline_button.callback_data

    return filters.create(func, "InlineButtonFilter", inline_button=inline_button)
