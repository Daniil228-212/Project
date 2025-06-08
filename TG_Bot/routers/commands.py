from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from TG_Bot.keyboards.inline import main_menu_keyboard
router = Router()
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в бота для анализа ставок BetBoom!\n"
        "Я помогу вам анализировать коэффициенты и делать ставки.",
        reply_markup=main_menu_keyboard()
    )
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n"
        "/matches - показать текущие матчи\n"
        "/stats - статистика ваших ставок\n"
        "/history - история матчей"
    )