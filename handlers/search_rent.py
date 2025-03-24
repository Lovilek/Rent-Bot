from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import get_navigation_kb
from services.filters import search_apartments
from utils.validators import normalize_price

router = Router()

class SearchApartment(StatesGroup):
    city = State()
    max_price = State()
    min_rooms = State()
    results = State()

@router.message(F.text == "/search")
async def start_search(message: Message, state: FSMContext):
    await message.answer("🔍 Введите город:")
    await state.set_state(SearchApartment.city)

@router.message(SearchApartment.city, F.text)
async def set_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.strip().capitalize())
    await message.answer("💰 Введите максимальную цену:")
    await state.set_state(SearchApartment.max_price)

@router.message(SearchApartment.max_price, F.text)
async def set_max_price(message: Message, state: FSMContext):
    price=normalize_price(message.text)
    if price is None:
        return await message.answer("Цена должна быть числом.")
    await state.update_data(max_price=price)
    await message.answer("🏠 Введите минимальное количество комнат:")
    await state.set_state(SearchApartment.min_rooms)

@router.message(SearchApartment.min_rooms, F.text)
async def set_min_rooms(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите число.")
    await state.update_data(min_rooms=int(message.text))

    data = await state.get_data()
    results = await search_apartments(data["city"], data["max_price"], data["min_rooms"])

    if not results:
        await message.answer("😢 Квартиры по вашему запросу не найдены.")
        await state.clear()
        return

    await state.update_data(results=results, index=0)
    apartment = results[0]
    caption = (
        f"📍 <b>{apartment['city']}</b>\n"
        f"💵 {apartment['price']} тг\n"
        f"🏠 {apartment['rooms']} комнатная\n"
        f"📝 {apartment['description']}\n"
        f"📍 {apartment['address']}\n"
        f"📞 {apartment['phone']}"
    )

    if apartment["photo"]:
        await message.answer_photo(apartment["photo"], caption=caption, reply_markup=get_navigation_kb())
    else:
        await message.answer(caption, reply_markup=get_navigation_kb())

    await state.set_state(SearchApartment.results)



@router.callback_query(SearchApartment.results, F.data.in_({"next", "prev"}))
async def navigate_results(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    results = data["results"]
    index = data.get("index", 0)

    if callback.data == "next":
        index = (index + 1) % len(results)
    elif callback.data == "prev":
        index = (index - 1) % len(results)

    apartment = results[index]
    caption = (
        f"📍 <b>{apartment['city']}</b>\n"
        f"💵 {apartment['price']} тг\n"
        f"🏠 {apartment['rooms']} комнат\n"
        f"📝 {apartment['description']}\n"
        f"📍 {apartment['address']}\n"
        f"📞 {apartment['phone']}"

    )

    if apartment["photo"]:
        await callback.message.answer_photo(apartment["photo"], caption=caption, reply_markup=get_navigation_kb())
    else:
        await callback.message.answer(caption, reply_markup=get_navigation_kb())

    await state.update_data(index=index)
    await callback.answer()
