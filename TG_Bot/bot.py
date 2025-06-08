import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import BOT_TOKEN
from routers.commands import router as commands_router
from routers.handlers import router as handlers_router
#from middlewares.throttling import ThrottlingMiddleware
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        filename="bot.log"
    )
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    #dp.message.middleware(ThrottlingMiddleware())
    dp.include_router(commands_router)
    dp.include_router(handlers_router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())