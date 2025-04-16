from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import requests
from aiogram.utils.keyboard import InlineKeyboardBuilder

link = "https://fakestoreapi.com/products"

response = requests.get(url=link).json()

def productbutton():
    buttons = InlineKeyboardBuilder()
    for i in response:
        buttons.add(InlineKeyboardButton(text=f"{i['title'][:8]}", callback_data=f"{i['title'][:8]}"))
    buttons.add(InlineKeyboardButton(text="ortga", callback_data="ortga"))
    buttons.adjust(2)
    return buttons.as_markup()

def SonlarButtons():
    buttons = InlineKeyboardBuilder()
    for i in range(1, 10):
        buttons.add(InlineKeyboardButton(text=f"{i}", callback_data=f"{i}"))
    buttons.add(InlineKeyboardButton(text="ortga", callback_data="ortga"))
    buttons.adjust(3)
    return buttons.as_markup()

menyu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Menyu", callback_data='menyu'), InlineKeyboardButton(text="Savat", callback_data="savat")],
        [InlineKeyboardButton(text='Bog\'lanish', callback_data="bog")]
    ]
)



buyurtma = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="buyurtma berish", callback_data="buyurtma"), InlineKeyboardButton(text="savat tozalash", callback_data="tozalash")]
    ]
)

ContactPhone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Contact", request_contact=True)]
    ],
    resize_keyboard=True
)


LocationButtons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Location", request_location=True)]
    ],
    resize_keyboard=True
)