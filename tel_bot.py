
import asyncio
from aiogram import Bot, Dispatcher, types
import logging
from aiogram.utils import executor
import os
from dotenv import load_dotenv
from ModelQA import *


users_data = {}


def tel_bot():
    load_dotenv()

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot)


    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
       # print(message.chat.id)
        await message.answer("Привет! Я бот, который может помочь ответить на все ваши вопросы 🤗")

    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def text_message(message: types.Message):
        await message.answer(question_response(sbert_embeddings, message.text))


    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    tel_bot()