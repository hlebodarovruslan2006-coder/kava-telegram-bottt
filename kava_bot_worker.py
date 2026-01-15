import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Настройки ---
TOKEN = os.getenv("TOKEN")  # Telegram токен через Environment Variable
ADMIN_CHAT_ID = 687268108

# --- Меню и подменю ---
def main_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Коляски", callback_data="menu_strollers")],
            [InlineKeyboardButton("Качели", callback_data="menu_swings")],
            [InlineKeyboardButton("Весы и шезлонг", callback_data="menu_scales")],
        ]
    )

strollers_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("BABALO 1300/2700₽", callback_data='order_BABALO')],
    [InlineKeyboardButton("Назад", callback_data='back_main')]
])

swings_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("AMAROBABY 1000/1600₽", callback_data='order_AMAROBABY')],
    [InlineKeyboardButton("4MOMS 1500/3000₽", callback_data='order_4MOMS')],
    [InlineKeyboardButton("BABYTON 700/1400₽", callback_data='order_BABYTON')],
    [InlineKeyboardButton("Назад", callback_data='back_main')]
])

scales_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("ВЕСЫ B1-15-САША 600/1300₽", callback_data='order_ВЕСЫ')],
    [InlineKeyboardButton("ШЕЗЛОНГ 700/1400₽", callback_data='order_ШЕЗЛОНГ')],
    [InlineKeyboardButton("Назад", callback_data='back_main')]
])

# --- Функции ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите категорию:", reply_markup=main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_strollers":
        await query.edit_message_text("Выберите модель коляски:", reply_markup=strollers_menu)
    elif data == "menu_swings":
        await query.edit_message_text("Выберите модель качели:", reply_markup=swings_menu)
    elif data == "menu_scales":
        await query.edit_message_text("Выберите модель весов:", reply_markup=scales_menu)
    elif data.startswith("order_"):
        user = query.from_user
        order_text = f"🛒 Новый заказ от @{user.username or user.first_name}:\n{data.replace('order_', '').replace('_', ' ')}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=order_text)
        await query.edit_message_text(f"Вы выбрали {data.replace('order_', '').replace('_', ' ')}. Менеджер свяжется с вами!")
    elif data == "back_main":
        await query.edit_message_text("Вы вернулись в главное меню:", reply_markup=main_menu())

# --- Основная логика ---
def main():
    if not TOKEN:
        raise RuntimeError("TOKEN not found in environment variables")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()  # Background Worker запускает polling без веб-порта

if __name__ == "__main__":
    main()
