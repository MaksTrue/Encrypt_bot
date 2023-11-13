import SQL_DB
import sqlite3
import asyncio
import logging
import sys
import os
import Buttons as bt
import States as st
import Texts as txt
import Encrypt as en
import Decrypt as de

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types.message import ContentType
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

load_dotenv()
bot = Bot(os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher()
PAYMENTS_TOKEN = "381764678:TEST:71271"

price = types.LabeledPrice(label="Подписка на 1 месяц", amount=1000 * 100)  # в копейках (руб)

#@NeroTekE_bot (https://t.me/NeroTekE_bot) - название бота

# sql_db = SQL_DB.Data_Base()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.reply(f'Добро пожаловать, {hbold(message.from_user.full_name)} !\n'
                        f'\n'
                        f'{txt.greeting_message}', reply_markup=bt.keyboard)


@dp.message(Command('buy'))
async def buy(message: types.Message):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[price],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


async def shifr_message(message: Message, state: FSMContext):
    text_input = await en.message_input(message.text.split('#')[0], int(message.text.split('#')[1]))
    await message.answer(text_input)
    # await sql_db.add_data_shifr(message.from_user.id, message.text.split('#')[0], int(message.text.split('#')[1]),text_input)
    await state.clear()


async def deshifr_message(message: Message, state: FSMContext):
    text_output = await de.message_output(message.text.split('#')[0], int(message.text.split('#')[1]))
    await message.answer(text_output)
    # await sql_db.add_data_deshifr(message.from_user.id, message.text.split('#')[0], int(message.text.split('#')[1]),text_output)
    await state.clear()


@dp.message(F.text.lower() == '🔐 зашифровать сообщение')
async def encrypt(message: types.Message, state: FSMContext):
    await state.set_state(st.States.shifr)
    await message.answer(f'{txt.shifr_text}')


@dp.message(F.text.lower() == '🔓 расшифровать сообщение')
async def decrypt(message: types.Message, state: FSMContext):
    await state.set_state(st.States.deshifr)
    await message.answer(f'{txt.deshifr_text}')


@dp.message(F.text.lower() == '💰 подписка')
async def subscription(message: types.Message, state: FSMContext):
    await state.set_state(st.States.subscription)
    await message.answer(f'{txt.subscription}')


@dp.message(F.text.lower() == '🛠 обратная связь')
async def feedback(message: types.Message, state: FSMContext):
    await state.set_state(st.States.feedback)
    await message.answer('Функционал не реализован, попробуйте позже.')


@dp.message(F.text.lower() == '📄 описание')
async def description(message: types.Message, state: FSMContext):
    await state.set_state(st.States.description)
    await message.answer(f'{txt.description}')


@dp.message(F.text.lower() == '❌ удалить переписку')
async def delete(message: types.Message, state: FSMContext):
    await state.set_state(st.States.delete)
    await message.answer('Функционал не реализован, попробуйте позже.')


dp.message.register(shifr_message, st.States.shifr)
dp.message.register(deshifr_message, st.States.deshifr)
dp.message.register(subscription, st.States.subscription)
dp.message.register(feedback, st.States.feedback)
dp.message.register(description, st.States.description)
dp.message.register(delete, st.States.delete)


@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message()
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100}"
                           f" {message.successful_payment.currency} прошел успешно!!!")


# TODO: Подключить Юмани
# TODO: Сделать счетчик тестового периода, например тестовый период 2 дня, потом нужно оплачивать подписку
# TODO: Залить на сервер
# TODO: Сделать инлайн кнопки
# TODO: Очистка основного чата с ботом '❌ удалить переписку'
# TODO: ***сделать отдельный чат с обратной связью и чатом или сделать отдельного бота,
#  где будт приниматься только сообщения от пользователей и размещаться реклама с обновлениями и информацией
# TODO: Сделать отдельные ссылки на комнаты, в них будут фиксированные ключи шифрования.
#  Пользователи смогут сразу общаться зашиброванными сообщениями. После выхода из комнаты вся переписка удаляется.


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
