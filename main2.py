from aiogram import Dispatcher, Bot, F
import logging
import asyncio
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from config import token, admin
from inline_pagination import link, get_pagination_keyboard



bot = Bot(token=token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command('start'))
async def StartBot(mes: Message):
    await mes.answer_photo(
        photo=link[0],
        caption="Rasmlar ro'yxati\nBu 1",
        reply_markup=get_pagination_keyboard(0)
    )
    await mes.answer("Assalomu alaykum Botga xush kelibsiz")



@dp.callback_query(lambda c: c.data.startswith('page_'))
async def process_callback(callback_query: CallbackQuery):
    print(callback_query.data)
    current_page = int(callback_query.data.split('_')[1])
    await callback_query.message.edit_media(
        InputMediaPhoto(
            media=link[current_page],
            caption=f"Rasmlar ro'yxati\nBu {current_page + 1}"
        ),
        reply_markup=get_pagination_keyboard(current_page)
    )

    await callback_query.answer()


async def main():
    await bot.send_message(chat_id=admin[0], text="Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print("tugadi")

