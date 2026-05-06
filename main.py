import asyncio
import csv
import os
# import psycopg2

from datetime import datetime

from aiogram.types import FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv, set_key
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject

load_dotenv()

def get_admin_id():
    return int(os.getenv("ADMIN_ID"))

GROUP_ID = os.getenv('DEPARTAMENT_GROUP')
TOPIC_ID = os.getenv('DEPARTAMENT_TOPIC')

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

shaurma_list = [
    "Большая",
    "Средняя",
    "Тропическая",
    "Лахмаджун",
    "Гирос",
    "Половинка",
    "Другое",
    "НЕТ"
]

DB_CONFIG = {
    "host": os.getenv('DB_HOST'),
    "port": os.getenv('DB_PORT'),
    "dbname": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASS'),
}


# def save_to_db(results, date):
#     conn = psycopg2.connect(**DB_CONFIG)
#     cursor = conn.cursor()
#
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS food_orders (
#             id SERIAL PRIMARY KEY,
#             consumer TEXT,
#             product TEXT,
#             order_date DATE
#         )
#     """)
#
#     current_results = []
#     for consumer_id, info in results.items():
#         consumer = info['consumer']
#
#         products = [p for p in info['product'].split() if p]
#
#         for product in products:
#             current_results.append({
#                 'consumer': consumer,
#                 'product': product
#             })
#
#     insert_query = "INSERT INTO food_orders (consumer, product, order_date) VALUES (%s, %s, %s)"
#     data_to_insert = [
#         (res['consumer'], res['product'], date)
#         for res in current_results
#     ]
#
#     cursor.executemany(insert_query, data_to_insert)
#
#     conn.commit()
#     cursor.close()
#     conn.close()


def save_to_csv(results, date):
    current_results = []
    for consumer_id, info in results.items():
        consumer = info['consumer']

        products = [p for p in info['product'].split() if p]

        for product in products:
            current_results.append({
                'consumer': consumer,
                'product': product,
                'date': date
            })

    file_path = 'food_basket.csv'
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['consumer', 'product', 'date'],
            delimiter=';'
        )
        writer.writerows(current_results)


active_poll = {}


@dp.message(Command("shaurma"), F.from_user.id == get_admin_id())
async def cmd_create_poll(message: types.Message):
    if active_poll:
        await message.answer("Уже есть активный опрос!")
        return

    await message.answer('Создаю опрос')
    poll_message = await bot.send_poll(
        chat_id=GROUP_ID,
        message_thread_id=TOPIC_ID,
        question="Шаурма?",
        options=shaurma_list,
        is_anonymous=False,
        allows_multiple_answers=True
    )

    active_poll["id"] = poll_message.poll.id
    active_poll["message_id"] = poll_message.message_id
    active_poll["results"] = {}


@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    if active_poll.get("id") == poll_answer.poll_id:
        print('Новый ответ в опросе!')
        user_info = f"{poll_answer.user.full_name} (@{poll_answer.user.username})"
        selected_products = ''
        for i in poll_answer.option_ids:
            selected_products += f'{shaurma_list[i]} '

        print(f'{user_info} - {selected_products}')
        active_poll["results"][poll_answer.user.id] = {
            "consumer": user_info,
            "product": selected_products
        }


@dp.message(Command("stop_shaurma"), F.from_user.id == get_admin_id())
async def cmd_stop_poll(message: types.Message):
    if not active_poll:
        await message.answer("Нет активных опросов.")
        return

    current_results = active_poll["results"]
    poll_msg_id = active_poll["message_id"]

    await bot.stop_poll(chat_id=GROUP_ID, message_id=poll_msg_id)
    await message.answer("Опрос закрыт")

    await bot.forward_message(
        chat_id=get_admin_id(),
        from_chat_id=GROUP_ID,
        message_id=active_poll["message_id"]
    )

    today = datetime.now().strftime("%Y-%m-%d")
    try:
        save_to_csv(current_results, today)
        # save_to_db(current_results, today)
        await message.answer("Данные успешно сохранены")
        active_poll.clear()
    except Exception as e:
        print(f"Ошибка при загрузке в БД: {e}")


@dp.message(Command("get_my_id"))
async def get_my_id(message: types.Message):
    await message.answer(f"User Name: {message.from_user.full_name}\nUser ID: {message.from_user.id}")


@dp.message(Command("send"), F.from_user.id == get_admin_id())
async def send_to_topic(message: types.Message, command: CommandObject):
    if not command.args:
        return await message.answer("Использование: /send Ваш текст")

    try:
        await bot.send_message(
            chat_id=GROUP_ID,
            text=command.args,
            message_thread_id=TOPIC_ID
        )
        await message.answer("✅ Сообщение отправлено в группу!")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке: {e}")


@dp.message(F.photo, Command("sendpic"), F.from_user.id == get_admin_id())
async def send_photo_to_topic(message: types.Message, command: CommandObject):
    photo_id = message.photo[-1].file_id
    # Текст после команды
    description = command.args if command.args else ""

    try:
        await bot.send_photo(
            chat_id=GROUP_ID,
            photo=photo_id,
            caption=description,
            message_thread_id=TOPIC_ID
        )
        await message.answer("✅ Фото успешно отправлено в тему!")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@dp.message(Command("get_data"))
async def send_csv(message: types.Message):
    file_path = "food_basket.csv"

    try:
        document = FSInputFile(file_path)
        await message.answer_document(
            document
        )
    except Exception as e:
        await message.answer(f"Ошибка при отправке файла: {e}")


pending_updates = {}
@dp.message(F.text.startswith(os.getenv("ADMIN_WORD")))
async def request_admin_change(message: types.Message):
    if message.from_user.id != get_admin_id():
        await message.answer("Забудь это слово")
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Добавь id после слова")
        return

    new_id = parts[1]
    pending_updates[message.from_user.id] = new_id

    # Создаем кнопку подтверждения
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"Да, сменить на {new_id}")
    builder.button(text="Отмена")

    await message.answer(
        f"⚠️ Вы уверены?\nТекущий ID: {get_admin_id()}\nНовый ID: {new_id}\n\n"
        "После подтверждения вы потеряете доступ к боту",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )


@dp.message(F.text.startswith("Да, сменить на"))
async def confirm_admin_change(message: types.Message):
    user_id = message.from_user.id

    if user_id not in pending_updates:
        await message.answer("Сначала введите команду обновления")
        return

    new_id = pending_updates.pop(user_id)
    os.environ["ADMIN_ID"] = new_id
    try:
        set_key('.env', "ADMIN_ID", new_id)
        await message.answer(
            f"✅ Успешно!\nADMIN_ID изменен на {new_id}",
            reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка записи: {e}")


@dp.message(F.text == "Отмена")
async def cancel_update(message: types.Message):
    pending_updates.pop(message.from_user.id, None)
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def main():
    print('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())