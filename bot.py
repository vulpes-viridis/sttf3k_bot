from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from fetch import fetch_timetable, find_date
from key import _key

app = ApplicationBuilder().token(_key).build()


async def fetch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Верхнюю", callback_data="v"),
            InlineKeyboardButton("Нижнюю", callback_data="n"),
        ],
        [InlineKeyboardButton("А, не, не надо)", callback_data="cancel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Какую неделю?", reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data in "vn":
        path = fetch_timetable(query.data)
        caption = f"Вот расписание с {find_date()}:"
        with open(path, "rb") as photo:
            await query.message.reply_photo(photo=photo, caption=caption)

    else:
        await query.message.delete()


app.add_handler(CommandHandler("fetch", fetch))
app.add_handler(CallbackQueryHandler(button_callback))

app.run_polling()
