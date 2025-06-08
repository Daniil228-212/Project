from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
def main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Текущие матчи", callback_data="get_matches")],
        [InlineKeyboardButton(text="Рекомендации", callback_data="get_recommendations")],
        [InlineKeyboardButton(text="История просмотров", callback_data="view_history")],
        [InlineKeyboardButton(text="Перейти на BetBoom", url="https://betboom.ru")]
    ])