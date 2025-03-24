from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_navigation_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev"),
            InlineKeyboardButton(text="➡️ Далее", callback_data="next")
        ]
    ])

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_delete_kb(apartment_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{apartment_id}")]
    ])
