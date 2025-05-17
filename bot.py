import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
import asyncio

from panic_parser import parse_panic_file
from db import get_error_tips

TOKEN = "7150429783:AAG_t8pbChxSEK008aCoGmvyHpjDcUQ84qk"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привіт! Надішліть файл panic (.ips або .txt) для аналізу.")

@dp.message(lambda message: message.document)
async def handle_document(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)
    file_text = file_bytes.read().decode('utf-8', errors='ignore')

    info = parse_panic_file(file_text)
    tips = get_error_tips(info["errors"])

    result = (
        f"Інформація про пристрій:\n"
        f"📱 Модель: {info['model']}\n"
        f"🛠️ Версія iOS: {info['ios']}\n"
        f"📅 Дата збою: {info['date']}\n\n"
        f"Найденные ошибки и рекомендации по ремонту:\n"
    )
    if tips:
        for t in tips:
            result += f"- {t}\n"
    else:
        result += "Не знайдено відповідних порад у базі."

    await message.answer(result)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
