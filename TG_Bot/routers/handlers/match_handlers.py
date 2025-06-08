from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from TG_Bot.services.betboom_parser import BetBoomService
router = Router()
@router.message(F.text == "Матчи")
async def show_matches(message: Message):
    service = BetBoomService()
    df = service.scrape_betboom()
    if df.empty:
        await message.answer("Не удалось получить данные о матчах. Попробуйте позже.")
        return
    response = "⚽ Актуальные матчи (BetBoom):\n\n"
    for _, row in df.head(5).iterrows():
        response += (
            f"{row['team1']} vs {row['team2']}\n"
            f"П1: {row['coeff_win1']:.2f} | Ничья: {row['coeff_draw']:.2f} | П2: {row['coeff_win2']:.2f}\n"
            f"Ссылка: https://betboom.ru/search?q={row['team1']}+{row['team2']}\n\n"
        )
    await message.answer(response)
@router.callback_query(F.data == "get_matches")
async def send_matches_callback(callback: CallbackQuery):
    await show_matches(callback.message)