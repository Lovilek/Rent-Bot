from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.db import get_user_apartments, delete_apartment_by_id
from keyboards.inline import get_delete_kb

router = Router()

@router.message(F.text == "/my")
async def show_my_apartments(message: Message):
    apartments = await get_user_apartments(message.from_user.id)
    if not apartments:
        return await message.answer("У вас пока нет добавленных квартир.")

    for apt in apartments:
        caption = (
            f"🏘 <b>{apt['city'].capitalize()}</b>\n"
            f"📍 Адрес: {apt['address']}\n"
            f"💵 {apt['price']} тг\n"
            f"🏠 Комнат: {apt['rooms']}\n"
            f"☎️ Телефон: {apt['phone']}\n"
            f"📝 {apt['description']}"
        )
        if apt['photo']:
            await message.answer_photo(apt['photo'], caption=caption, reply_markup=get_delete_kb(apt['id']))
        else:
            await message.answer(caption, reply_markup=get_delete_kb(apt['id']))

@router.callback_query(F.data.startswith("delete_"))
async def delete_apartment(callback: CallbackQuery):
    apt_id = int(callback.data.replace("delete_", ""))
    deleted = await delete_apartment_by_id(apt_id, callback.from_user.id)

    if deleted:
        await callback.message.edit_caption("❌ Квартира удалена.")
    else:
        await callback.answer("Не удалось удалить. Возможно, это не ваша квартира.", show_alert=True)
