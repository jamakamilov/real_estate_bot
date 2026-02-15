from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def approve_keyboard(listing_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Одобрить",
                callback_data=f"approve_{listing_id}"
            ),
            InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"reject_{listing_id}"
            )
        ]
    ])

def boost_keyboard(listing_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 Поднять",
                callback_data=f"boost_{listing_id}"
            )
        ]
    ])
