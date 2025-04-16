import logging
import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart
from config import token, admin
from buttons import menyu, productbutton, SonlarButtons, buyurtma, ContactPhone, LocationButtons
from state import Sotibolish, Zakaz
from aiogram.fsm.context import FSMContext
import requests
from database import AddSavat, ReadSavat, SavatClear
from pyments import Product

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
    if len(malumotlar) >= 1:
        text = "Nomi    |    Narxi    |    Soni   |  Jami summasi  |\n\n"
        summ = 0
        for i in malumotlar:
            text  += f"{i[1]}    |     {i[2]}$    |      {i[3]}      |       {float(i[2] * int(i[3]))} $ |\n"
            summ += float(i[2] * int(i[3]))
        await call.message.answer_photo(photo="https://api.korzinka.uz/upload/uf/9a9/llqc0jhen5efm6jum3tpj1x39ph6upyz.jpg", caption=f"{text}\nJami summa {summ} $", reply_markup=buyurtma)    
    else:
        await call.answer("Savatingiz bosh")


@dp.callback_query(F.data=="tozalash")
async def BuyurtmaBot(call: CallbackQuery):
    user_id = call.from_user.id
    SavatClear(user_id=user_id)
    await call.message.answer_photo(photo="https://postium.ru/wp-content/uploads/2024/06/dostavka-edy.jpg", caption="Assalomu alaykum bizning dastafka botga xush kelibsiz\n", reply_markup=menyu)


@dp.callback_query(F.data=="buyurtma")
async def BuyurtmaQilishBot(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Telefon nomeringizni yuboring ?", reply_markup=ContactPhone)
    await state.set_state(Zakaz.contact)




@dp.message(Zakaz.contact)
async def ContactPHone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await message.answer("Locatsiya yuboring ?", reply_markup=LocationButtons)
    await state.update_data(phone = phone)
    await state.set_state(Zakaz.location)


@dp.message(Zakaz.location)
async def ZakazLocation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    la = message.location.latitude
    lo = message.location.longitude
    await state.update_data(lo=lo, la=la)
    malumotlar = ReadSavat(id=user_id)
    summ = 0
    for i in malumotlar:
        summ += float(i[2] * int(i[3])) 
    prices = [LabeledPrice(label="Sotuv summasi", amount=summ*100)] 
    invoice = Product(title="Buyurma berilyabdi", description="Siz sotib olmoqchi bo'lgan maxsulotlaringizni tasdiqlash", start_parameter="Tasdiqlash", currency="UZS", prices=prices, need_email=True, need_name=True, need_phone_number=True, need_shipping_address=True, is_flexible=True)
    await bot.send_invoice(chat_id=user_id, **invoice.generate_invoice(), payload=f"payload_maxsulotlar")
    await state.clear()
    
@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message()
async def successful_payment(message: Message):
    if message.successful_payment:
        amount = message.successful_payment.total_amount / 100  # Tiyindan so‘mga o‘tkazish
        await message.answer(f"To'lovingiz uchun rahmat! Siz {amount} so'm to‘lov qildingiz.")
        await bot.send_message(chat_id=admin[0], text=f"ismi: {message.from_user.full_name}\nuser id: {message.from_user.id}\nsumma: {amount} so'm\no'tkazildi")



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



