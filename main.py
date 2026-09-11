import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from ai import solve_task
from geometry_draw import draw_geometry


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def main():

    session = AiohttpSession()

    bot = Bot(
        token=TOKEN,
        session=session
    )

    dp = Dispatcher()


    @dp.message(Command("start"))
    async def start(message: Message):

        await message.answer("Бот работает 🤖")



    @dp.message()
    async def answer(message: Message):

        await message.answer("Решаю задачу...")


        photo_path = None


        # Если пользователь отправил фото

        if message.photo:


            photo = message.photo[-1]


            file = await bot.get_file(
                photo.file_id
            )


            photo_path = f"task_photo_{message.from_user.id}_{message.message_id}.jpg"


            await bot.download_file(
                file.file_path,
                photo_path
            )


            result = await solve_task(
                message.caption if message.caption else None,
                photo_path
            )


        else:


            result = await solve_task(
                message.text,
                None
            )



        geometry_data = None



        # Проверяем геометрию

        if "<GEOMETRY_DATA>" in result:



            student_text = (
                result
                .split("<GEOMETRY_DATA>")[0]
            )



            geometry_data = (
                result
                .split("<GEOMETRY_DATA>")[1]
                .split("</GEOMETRY_DATA>")[0]
            )


            print("ПОЛУЧИЛИ:")
            print(geometry_data)


            print("\n===== ДАННЫЕ ЧЕРТЕЖА =====")
            print(geometry_data)
            print("===========================\n")



        else:


            student_text = result





        # Отправляем решение

        await message.answer(
            student_text
        )





        # Создаем чертеж

        if geometry_data:


            try:


                image_path = draw_geometry(
                    geometry_data
                )


                photo = FSInputFile(
                    image_path
                )


                await message.answer_photo(
                    photo,
                    caption="📐 Чертёж"
                )



            except Exception as e:


                print(
                    "Ошибка создания чертежа:",
                    e
                )



        # Удаляем фото задачи после обработки

        if photo_path:

            try:

                os.remove(photo_path)

                print(
                    "Фото удалено:",
                    photo_path
                )


            except Exception as e:

                print(
                    "Ошибка удаления фото:",
                    e
                )



    print("Бот запущен")


    await dp.start_polling(bot)




if __name__ == "__main__":

    asyncio.run(main())