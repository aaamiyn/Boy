import telebot
from config import TOKEN
from database import init_db
from handlers import register_handlers

# 1. Ma'lumotlar bazasini tayyorlash
init_db()

# 2. Botni ishga tushirish
bot = telebot.TeleBot(TOKEN)

# 3. Buyruqlarni ro'yxatdan o'tkazish
register_handlers(bot)

print("--- BOY tizimi ishga tushdi ---")
print("Bot hozir Telegramda xabarlarni kutmoqda...")

bot.infinity_polling()