import logging
from asyncio import sleep
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.dispatcher import FSMContext

API_TOKEN = os.getenv("api_bot")# '1732076175:AAGILnWtAxrxd_Dg5KpJNy_yUdLYE1HXzZI'  # os.getenv("api_bot")

logging.basicConfig(level=logging.INFO)
WEBHOOK_HOST = 'https://hisob-bot.herokuapp.com' 
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# States
class Kirim(StatesGroup):
    kirim = State()  # Will be represented in storage as 'Form:name'


class Chiqim(StatesGroup):
    chiqim = State()  # Will be represented in storage as 'Form:name'
    uy = State()  # Will be represented in storage as 'Form:age'
    ozim = State()  # Will be represented in storage as 'Form:gender'


class Jami(StatesGroup):
    jami = State()
    kirim_h = State()  # Will be represented in storage as 'Form:name'
    chiqim_h = State()  # Will be represented in storage as 'Form:age'
    hammasi = State()  # Will be represented in storage as 'Form:gender'


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    msg = 'Botga hush kelibsz'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Kirim", "Chiqim")
    markup.add("Jami")
    await message.answer(msg, reply_markup=markup)


@dp.message_handler(state='*',commands=['qaytish'])
@dp.message_handler(state='*',text=['Qaytish'])
async def go_qaytish(message: types.Message, state: FSMContext):
    await state.finish()
    msg = 'siz bosh menu dasiz'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Kirim", "Chiqim")
    markup.add("Jami")
    await message.answer(msg, reply_markup=markup)


@dp.message_handler(commands=['kirim'])
@dp.message_handler(text=['Kirim'])
async def go_kirim(message: types.Message):
    await Kirim.kirim.set()
    msg = 'iltimos malumot kiriting'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Qaytish")
    await message.answer(msg, reply_markup=markup)


@dp.message_handler(commands=['chiqim'])
@dp.message_handler(text=['Chiqim'])
async def go_chiqim(message: types.Message):
    msg = 'Bo\'limni tanlang'
    await Chiqim.chiqim.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("uy", "ozimga")
    markup.add("Qaytish")

    await message.answer(msg, reply_markup=markup)


@dp.message_handler(commands=['jami'])
@dp.message_handler(text=['Jami'])
async def go_jami(message: types.Message):
    msg = 'Bo\'limni tanlang'
    await Jami.jami.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Kirimlar uchun")
    markup.add("Chiqimlar uchun")
    markup.add("Hammasi")
    markup.add("Qaytish")

    await message.answer(msg, reply_markup=markup)


@dp.message_handler(text=['Hammasi'], state=Jami.jami)
async def go_jami(message: types.Message, state: FSMContext):
    msg = 'Hamma kirim chiqimlar korinadi'
    await state.finish()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Kirimlar uchun")
    markup.add("Chiqimlar uchun")
    markup.add("Hammasi")
    markup.add("Qaytish")

    await message.answer(msg, types.ReplyKeyboardRemove())

@dp.message_handler(text='kurs')
async def kurs(message: types.Message):
    pass


@dp.message_handler()
async def echo(message: types.Message):
    pass


async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    try:
        await bot.set_webhook(WEBHOOK_URL)
    except Exception:
        print('XAto boldi bu ish bolmadi')
    await bot.send_message(711910507, "Men ishga tushdim")


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')
    await bot.send_message(711910507, "Men o'chyapman")
    # await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT, )
