from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Я помогу тебе найти или сдать квартиру.\n\n"
        f"Команды:\n"
        f"/add — добавить квартиру\n"
        f"/search — найти квартиру\n"
        f"/my - список ваших квартир"
    )
