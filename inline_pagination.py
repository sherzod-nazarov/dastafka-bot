from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

link = [
    "https://buffer.com/cdn-cgi/image/w=1000,fit=contain,q=90,f=auto/library/content/images/size/w1200/2023/10/free-images.jpg",
    "https://www.piclumen.com/wp-content/uploads/2024/08/ai-generated-female-with-wings-standing-on-the-woods.webp",
    "https://i.abcnewsfe.com/a/f43853f3-9eaf-4048-9ae7-757332c5787e/mclaren-1-ht-gmh-240412_1712928561648_hpMain_16x9.jpg?w=992",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScTgBHJddWcIEcxEYahoPIrO6KTb7LhrZM-g&s"

]



def get_pagination_keyboard(current_page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if current_page > 0:
        builder.add(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data=f"page_{current_page - 1}"
        ))
    builder.add(InlineKeyboardButton(
        text=f"{current_page + 1}/{len(link)}",
        callback_data="current_page"
    ))
    if current_page < len(link) - 1:
        builder.add(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data=f"page_{current_page + 1}"
        ))

    return builder.as_markup()