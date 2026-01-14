import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = 687268108

PHONE_LINK = "https://wa.me/79516382727"
INSTAGRAM_LINK = "https://www.instagram.com/kavakids03"

PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Коляски", callback_data="menu_strollers")],
        [InlineKeyboardButton("Качели", callback_data="menu_swings")],
        [InlineKeyboardButton("Весы и шезлонг", callback_data="menu_scales")],
        [InlineKeyboardButton("📞 WhatsApp", url=PHONE_LINK)],
        [InlineKeyboardButton("📷 Instagram", url=INSTAGRAM_LINK)],
    ])

strollers_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("BABALO — 1300/2700", callback_data="order_BABALO")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в KAVA 👶\nВыберите категорию:",
        reply_markup=main_menu()
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "menu_strollers":
        await q.edit_message_text("Выберите коляску:", reply_markup=strollers_menu)

    elif q.data.startswith("order_"):
        product = q.data.replace("order_", "")
        user = q.from_user

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🛒 Новый заказ\nОт: @{user.username or user.first_name}\nТовар: {product}"
        )

        await q.edit_message_text(
            f"✅ Вы выбрали: {product}\nМы скоро свяжемся с вами.",
            reply_markup=main_menu()
        )

    elif q.data == "back":
        await q.edit_message_text("Главное меню:", reply_markup=main_menu())

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
    )

if  __name__ == "__main__":
    main()
