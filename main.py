import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from routers import handler

TOKEN = "" # Telegram Bot token
USER_ID = ... # Your telegram user ID


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher()

    # dp.include_routers(handler.router)
    asyncio.create_task(handler.start_monitoring(bot=bot, user_id=USER_ID))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
