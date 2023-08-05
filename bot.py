from utils.config import Configuration
from utils.telegram_worker import TelegramWorker

from aiogram import Bot, Dispatcher, types


bot = Bot(token=Configuration.telegram_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['/start'])
async def start(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)
    await TelegramWorker.start(message)


@dp.message_handler(commands=['/reset_context'])
async def reset_context(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)
    await TelegramWorker.reset_context(message)


@dp.message_handler()
async def text(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action=types.ChatActions.TYPING)
    await TelegramWorker.gpt(message)
