from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import TOKEN
from handlers import start, add_rent,search_rent,my_rents
from database.db import init_db
import asyncio

async def on_startup(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="add", description="Добавить квартиру"),
        BotCommand(command="search", description="Поиск квартиры"),
        BotCommand(command="my",description="Список моих квартир")
    ])

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start.router,
        add_rent.router,
        search_rent.router,
        my_rents.router


    )
    await on_startup(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
