import os
import asyncio
import tempfile

from aiogram import Bot
from aiogram.types import FSInputFile

from ai import solve_task
from geometry_draw import draw_geometry


TOKEN = os.getenv("TELEGRAM_TOKEN")


async def process_update(update):

    bot = Bot(token=TOKEN)

    photo_path = None

    try:

        # =========================
        # /start
        # =========================

        if "message" not in update:
            return

        message = update["message"]

        chat = message["chat"]
        chat_id = chat["id"]

        # =========================
        # Команда /start
        # =========================

        text = message.get("text")

        if text == "/start":

            await bot.send_message(
                chat_id,
                "Бот работает 🤖"
            )

            return

        # =========================
        # Сообщение с фотографией
        # =========================

        if "photo" in message:

            photo = message["photo"][-1]

            file = await bot.get_file(
                photo["file_id"]
            )

            # В Cloud Functions используем /tmp
            photo_path = os.path.join(
                tempfile.gettempdir(),
                f"task_photo_{chat_id}.jpg"
            )

            await bot.download_file(
                file.file_path,
                photo_path
            )

            await bot.send_message(
                chat_id,
                "Решаю задачу... 🤖"
            )

            result = await solve_task(
                message.get("caption"),
                photo_path
            )

        # =========================
        # Обычный текст
        # =========================

        else:

            if not text:
                return

            await bot.send_message(
                chat_id,
                "Решаю задачу... 🤖"
            )

            result = await solve_task(
                text,
                None
            )

        # =========================
        # Проверяем геометрию
        # =========================

        geometry_data = None

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

            print("ДАННЫЕ ЧЕРТЕЖА:")
            print(geometry_data)

        else:

            student_text = result

        # =========================
        # Отправляем решение
        # =========================

        await bot.send_message(
            chat_id,
            student_text
        )

        # =========================
        # Создаём чертёж
        # =========================

        if geometry_data:

            try:

                image_path = draw_geometry(
                    geometry_data
                )

                photo = FSInputFile(
                    image_path
                )

                await bot.send_photo(
                    chat_id,
                    photo,
                    caption="📐 Чертёж"
                )

                # Удаляем созданный чертёж

                try:
                    os.remove(image_path)
                except Exception:
                    pass

            except Exception as e:

                print(
                    "Ошибка создания чертежа:",
                    e
                )

    except Exception as e:

        print(
            "Ошибка обработки:",
            e
        )

        try:

            await bot.send_message(
                chat_id,
                "Произошла ошибка при обработке задачи 😔"
            )

        except Exception:
            pass

    finally:

        # Удаляем загруженное пользователем фото

        if photo_path:

            try:
                os.remove(photo_path)
            except Exception:
                pass

        await bot.session.close()


def handler(event, context):

    asyncio.run(
        process_update(event)
    )

    return {
        "statusCode": 200,
        "body": ""
    }