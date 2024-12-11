import asyncio
import logging
import sys

from aiogram import Dispatcher, html, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from breeze_bot.infra.telegram.settings import BotSettings

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    bot_settings = BotSettings(token='7445022691:AAFkvSj2td8uX3zAJWVdPoSldy0UqWzBR5U')
    bot = Bot(token=bot_settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
