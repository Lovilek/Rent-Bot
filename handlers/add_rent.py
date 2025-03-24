from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.models import Apartment
from database.db import insert_apartment
from utils.validators import normalize_price

router = Router()

class AddApartment(StatesGroup):
    city = State()
    price = State()
    rooms = State()
    description = State()
    address = State()
    phone = State()
    photo = State()

@router.message(F.text == "/add")
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("🏙 Введите город:")
    await state.set_state(AddApartment.city)

@router.message(AddApartment.city, F.text)
async def step_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.strip().capitalize())
    await message.answer("💵 Введите цену (только цифры):")
    await state.set_state(AddApartment.price)



@router.message(AddApartment.price, F.text)
async def step_price(message: Message, state: FSMContext):
    price=normalize_price(message.text)
    if price is None:
        return await message.answer("Введите корректную цену (число):")
    await state.update_data(price=price)
    await message.answer("🏠 Сколько комнат?")
    await state.set_state(AddApartment.rooms)


@router.message(AddApartment.rooms, F.text)
async def step_rooms(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите количество комнат числом:")
    await state.update_data(rooms=int(message.text))
    await message.answer("📍 Введите адрес квартиры:")
    await state.set_state(AddApartment.address)

@router.message(AddApartment.address, F.text)
async def step_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await message.answer("📞 Введите номер телефона для связи:")
    await state.set_state(AddApartment.phone)

@router.message(AddApartment.phone, F.text)
async def step_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.answer("📝 Введите описание квартиры:")
    await state.set_state(AddApartment.description)


@router.message(AddApartment.description, F.text)
async def step_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📷 Пришли фото квартиры (или напиши 'нет'):")
    await state.set_state(AddApartment.photo)

@router.message(AddApartment.photo, F.photo | F.text)
async def step_photo(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.photo:
        photo_id = message.photo[-1].file_id
    elif message.text.lower() == "нет":
        photo_id = None
    else:
        return await message.answer("Пожалуйста, отправьте фото или напишите 'нет'.")

    apartment = Apartment(
        user_id=message.from_user.id,
        city=data["city"],
        price=data["price"],
        rooms=data["rooms"],
        address=data["address"],
        phone=data["phone"],
        description=data["description"],
        photo=photo_id
    )

    await insert_apartment(apartment)
    await message.answer("✅ Квартира успешно добавлена!")
    await state.clear()
