import logging
import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from config import token, admin
from buttons import menyu, productbutton, SonlarButtons, buyurtma
from state import Sotibolish
from aiogram.fsm.context import FSMContext
import requests
from database import AddSavat, ReadSavat


link = "https://fakestoreapi.com/products"

response = requests.get(url=link).json()




dp = Dispatcher()
bot= Bot(token=token)
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def StartBot(message: Message):
    await message.answer_photo(photo="https://postium.ru/wp-content/uploads/2024/06/dostavka-edy.jpg", caption="Assalomu alaykum bizning dastafka botga xush kelibsiz\n", reply_markup=menyu)


@dp.callback_query(F.data=="savat")
async def SavatBot(call: CallbackQuery):
    user_id= call.from_user.id
    malumotlar = ReadSavat(id=user_id)
    text = "Nomi    |    Narxi    |    Soni   |  Jami summasi  |\n\n"
    summ = 0
    for i in malumotlar:
        text  += f"{i[1]}    |     {i[2]}$    |      {i[3]}      |       {float(i[2] * int(i[3]))} $ |\n"
        summ += float(i[2] * int(i[3]))
    await call.message.answer_photo(photo="https://api.korzinka.uz/upload/uf/9a9/llqc0jhen5efm6jum3tpj1x39ph6upyz.jpg", caption=f"{text}\nJami summa {summ} $", reply_markup=buyurtma)    



@dp.callback_query(F.data=="menyu")
async def MenyuBot(call: CallbackQuery, state: FSMContext):
    await call.message.answer_photo(photo="https://russia-china.com/wp-content/uploads/2017/03/1475917624_1.jpg", caption="Maxsulotlardan birini tanlang", reply_markup=productbutton())
    await state.set_state(Sotibolish.name)


@dp.callback_query(F.data, Sotibolish.name)
async def SotibOlish(call: CallbackQuery, state: FSMContext):
    name = call.data
    await state.update_data(name=name)
    for res in response:
        if res['title'][:8] == name:
            await call.message.answer_photo(photo=res['image'], caption=f"Name: {res['title']}\nNarxi: {res['price']}", reply_markup=SonlarButtons())
            await state.update_data(narxi=res['price'])
            await state.set_state(Sotibolish.narxi)
            break
    else:
        await call.message.answer_photo(photo="https://russia-china.com/wp-content/uploads/2017/03/1475917624_1.jpg", caption="Maxsulotlardan birini tanlang", reply_markup=productbutton())
        await state.clear()


@dp.callback_query(Sotibolish.narxi)
async def NarxiBot(call: CallbackQuery, state: FSMContext):
    count = call.data
    if count.isdigit():
        data = await state.get_data()
        name = data.get('name')
        narxi = data.get("narxi")
        user_id = call.from_user.id
        AddSavat(name=name, narxi=narxi, count=count, user_id=user_id)
        await call.answer("Savatga qo'shildi", show_alert=True)
        await call.message.answer_photo(photo="https://postium.ru/wp-content/uploads/2024/06/dostavka-edy.jpg", caption="Assalomu alaykum bizning dastafka botga xush kelibsiz\n", reply_markup=menyu)
        await state.clear()
    else:
        await call.message.answer_photo(photo="https://russia-china.com/wp-content/uploads/2017/03/1475917624_1.jpg", caption="Maxsulotlardan birini tanlang", reply_markup=productbutton())
        await state.set_state(Sotibolish.name)


async def main():
    await bot.send_message(chat_id=admin[0], text="Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("tugadi")



